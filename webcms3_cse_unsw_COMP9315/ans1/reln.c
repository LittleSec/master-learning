// reln.c ... functions on Relations
// part of Multi-attribute Linear-hashed Files
// Last modified by John Shepherd, July 2019

#include "defs.h"
#include "reln.h"
#include "page.h"
#include "tuple.h"
#include "chvec.h"
#include "bits.h"
#include "hash.h"

#define HEADERSIZE (3*sizeof(Count)+sizeof(Offset))

struct RelnRep {
	Count  nattrs; // number of attributes
	Count  depth;  // depth of main data file
	Offset sp;     // split pointer
    Count  npages; // number of main data pages
    Count  ntups;  // total number of tuples
	ChVec  cv;     // choice vector
	char   mode;   // open for read/write
	FILE  *info;   // handle on info file
	FILE  *data;   // handle on data file
	FILE  *ovflow; // handle on ovflow file
};

// create a new relation (three files)

Status newRelation(char *name, Count nattrs, Count npages, Count d, char *cv)
{
    char fname[MAXFILENAME];
	Reln r = malloc(sizeof(struct RelnRep));
	r->nattrs = nattrs; r->depth = d; r->sp = 0;
	r->npages = npages; r->ntups = 0; r->mode = 'w';
	assert(r != NULL);
	if (parseChVec(r, cv, r->cv) != OK) return ~OK;
	sprintf(fname,"%s.info",name);
	r->info = fopen(fname,"w");
	assert(r->info != NULL);
	sprintf(fname,"%s.data",name);
	r->data = fopen(fname,"w");
	assert(r->data != NULL);
	sprintf(fname,"%s.ovflow",name);
	r->ovflow = fopen(fname,"w");
	assert(r->ovflow != NULL);
	int i;
	for (i = 0; i < npages; i++) addPage(r->data);
	closeRelation(r);
	return 0;
}

// check whether a relation already exists

Bool existsRelation(char *name)
{
	char fname[MAXFILENAME];
	sprintf(fname,"%s.info",name);
	FILE *f = fopen(fname,"r");
	if (f == NULL)
		return FALSE;
	else {
		fclose(f);
		return TRUE;
	}
}

// set up a relation descriptor from relation name
// open files, reads information from rel.info

Reln openRelation(char *name, char *mode)
{
	Reln r;
	r = malloc(sizeof(struct RelnRep));
	assert(r != NULL);
	char fname[MAXFILENAME];
	sprintf(fname,"%s.info",name);
	r->info = fopen(fname,mode);
	assert(r->info != NULL);
	sprintf(fname,"%s.data",name);
	r->data = fopen(fname,mode);
	assert(r->data != NULL);
	sprintf(fname,"%s.ovflow",name);
	r->ovflow = fopen(fname,mode);
	assert(r->ovflow != NULL);
	// Naughty: assumes Count and Offset are the same size
	int n = fread(r, sizeof(Count), 5, r->info);
	assert(n == 5);
	n = fread(r->cv, sizeof(ChVecItem), MAXCHVEC, r->info);
	assert(n == MAXCHVEC);
	r->mode = (mode[0] == 'w' || mode[1] =='+') ? 'w' : 'r';
	return r;
}

// release files and descriptor for an open relation
// copy latest information to .info file

void closeRelation(Reln r)
{
	// make sure updated global data is put in info
	// Naughty: assumes Count and Offset are the same size
	if (r->mode == 'w') {
		fseek(r->info, 0, SEEK_SET);
		// write out core relation info (#attr,#pages,d,sp)
		int n = fwrite(r, sizeof(Count), 5, r->info);
		assert(n == 5);
		// write out choice vector
		n = fwrite(r->cv, sizeof(ChVecItem), MAXCHVEC, r->info);
		assert(n == MAXCHVEC);
	}
	fclose(r->info);
	fclose(r->data);
	fclose(r->ovflow);
	free(r);
}

Count storeAllTuples(Page pg, Tuple *dest, Count st)
{
	Count ntups = pageNTuples(pg);
	char *c = pageData(pg);
	for (int i = 0; i < ntups; i++) {
		dest[st++] = copyString(c);
		c += strlen(c) + 1;
	}
	return st;
}

PageID addToRelation_1(Reln r, Tuple t)
{
	Bits h, p;
	// char buf[MAXBITS+1];
	h = tupleHash(r,t);
	if (r->depth == 0)
		p = 1;
	else {
		p = getLower(h, r->depth);
		if (p < r->sp) p = getLower(h, r->depth+1);
	}

	Page pg = getPage(r->data,p);
	if (addToPage(pg,t) == OK) {
		putPage(r->data,p,pg);
		r->ntups++;
		return p;
	}
	// primary data page full
	if (pageOvflow(pg) == NO_PAGE) {
		// add first overflow page in chain
		PageID newp = addPage(r->ovflow);
		pageSetOvflow(pg,newp);
		putPage(r->data,p,pg);
		Page newpg = getPage(r->ovflow,newp);
		// can't add to a new page; we have a problem
		if (addToPage(newpg,t) != OK) return NO_PAGE;
		putPage(r->ovflow,newp,newpg);
		r->ntups++;
		return p;
	}
	else {
		// scan overflow chain until we find space
		// worst case: add new ovflow page at end of chain
		Page ovpg, prevpg = NULL;
		PageID ovp, prevp = NO_PAGE;
		ovp = pageOvflow(pg);
		while (ovp != NO_PAGE) {
			ovpg = getPage(r->ovflow, ovp);
			if (addToPage(ovpg,t) != OK) {
				prevp = ovp; prevpg = ovpg;
				ovp = pageOvflow(ovpg);
			}
			else {
				if (prevpg != NULL) free(prevpg);
				putPage(r->ovflow,ovp,ovpg);
				r->ntups++;
				return p;
			}
		}
		// all overflow pages are full; add another to chain
		// at this point, there *must* be a prevpg
		assert(prevpg != NULL);
		// make new ovflow page
		PageID newp = addPage(r->ovflow);
		// insert tuple into new page
		Page newpg = getPage(r->ovflow,newp);
        if (addToPage(newpg,t) != OK) return NO_PAGE;
        putPage(r->ovflow,newp,newpg);
		// link to existing overflow chain
		pageSetOvflow(prevpg,newp);
		putPage(r->ovflow,prevp,prevpg);
        r->ntups++;
		return p;
	}
	return NO_PAGE;
}

void splitPage(Reln r)
{
	PageID pid = r->sp;
	Page pg = getPage(r->data, pid);
	// calculate num_of_alltuple
	Count num_of_alltuple = pageNTuples(pg);
	Page ovpg;
	PageID ovp = pageOvflow(pg);
	while (ovp != NO_PAGE) {
		ovpg = getPage(r->ovflow, ovp);
		num_of_alltuple += pageNTuples(ovpg);
		ovp = pageOvflow(ovpg);
		free(ovpg);
	}

	// get all tuple of this page(include ovflow page) and clean it!
	Tuple *alltuples = (Tuple *)malloc(num_of_alltuple*sizeof(Tuple));
	assert(alltuples != NULL);
	Count st = storeAllTuples(pg, alltuples, 0);	
	ovp = pageOvflow(pg);
    cleanPage(pg, r->data, pid); // will call putPage->free(pg)
	PageID next_ovp = pageOvflow(pg);	
	while (ovp != NO_PAGE) {
		ovpg = getPage(r->ovflow, ovp);
		next_ovp = pageOvflow(ovpg);
		st = storeAllTuples(ovpg, alltuples, st);
		cleanPage(ovpg, r->ovflow, ovp); // don't change ovp
		ovp = next_ovp;
	}
	r->ntups -= st;
	// insert all tuples again
	addPage(r->data);
	r->npages++;
	r->sp++;
	if (r->sp >= (1 << r->depth)) {
		r->sp = 0;
		r->depth++;
	}
	Count i = 0;
	Tuple curtuple;
	for (i = 0; i < num_of_alltuple; i ++) {
		curtuple = alltuples[i];
		addToRelation(r, curtuple);
		free(curtuple);
	}

	// free alltuples
	free(alltuples);
}

// insert a new tuple into a relation
// returns index of bucket where inserted
// - index always refers to a primary data page
// - the actual insertion page may be either a data page or an overflow page
// returns NO_PAGE if insert fails completely

PageID addToRelation(Reln r, Tuple t)
{
	PageID pid = addToRelation_1(r, t);
	if (pid != NO_PAGE) {
		Page pg = getPage(r->data, pid);
		Count pnt = pageNTuples(pg) - 1;
		Count c = 1024 / (10 * r->nattrs);
		if (pnt != 0 && pnt % c == 0) {
			splitPage(r);
		}
	}
	return pid;
}

// external interfaces for Reln data

FILE *dataFile(Reln r) { return r->data; }
FILE *ovflowFile(Reln r) { return r->ovflow; }
Count nattrs(Reln r) { return r->nattrs; }
Count npages(Reln r) { return r->npages; }
Count ntuples(Reln r) { return r->ntups; }
Count depth(Reln r)  { return r->depth; }
Count splitp(Reln r) { return r->sp; }
ChVecItem *chvec(Reln r)  { return r->cv; }


// displays info about open Reln

void relationStats(Reln r)
{
	printf("Global Info:\n");
	printf("#attrs:%d  #pages:%d  #tuples:%d  d:%d  sp:%d\n",
	       r->nattrs, r->npages, r->ntups, r->depth, r->sp);
	printf("Choice vector\n");
	printChVec(r->cv);
	printf("Bucket Info:\n");
	printf("%-4s %s\n","#","Info on pages in bucket");
	printf("%-4s %s\n","","(pageID,#tuples,freebytes,ovflow)");
	for (Offset pid = 0; pid < r->npages; pid++) {
		printf("[%2d]  ",pid);
		Page p = getPage(r->data, pid);
		Count ntups = pageNTuples(p);
		Count space = pageFreeSpace(p);
		Offset ovid = pageOvflow(p);
		printf("(d%d,%d,%d,%d)",pid,ntups,space,ovid);
		free(p);
		while (ovid != NO_PAGE) {
			Offset curid = ovid;
			p = getPage(r->ovflow, ovid);
			ntups = pageNTuples(p);
			space = pageFreeSpace(p);
			ovid = pageOvflow(p);
			printf(" -> (ov%d,%d,%d,%d)",curid,ntups,space,ovid);
			free(p);
		}
		putchar('\n');
	}
}
