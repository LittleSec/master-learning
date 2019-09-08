// query.c ... query scan functions
// part of Multi-attribute Linear-hashed Files
// Manage creating and using Query objects
// Last modified by John Shepherd, July 2019

#include "defs.h"
#include "query.h"
#include "reln.h"
#include "hash.h"
#include "tuple.h"
#include "bits.h"
#include "page.h"

// A suggestion ... you can change however you like

struct QueryRep {
	Reln    rel;       // need to remember Relation info
	PageID  curpageid; // current pageid in scan
	Page    curpage;   // current page in scan
	int     is_ovflow; // are we in the overflow pages?
	Offset  curtup;    // offset of current tuple within page
	
	Tuple   search_str;

	PageID  *all_possible_page;
	Offset  curpage_idx;
	Count   pagenum;   // len(all_possible_page)
};


void setQueryPageInfo(Query q, Bool is_ovpg)
{
	if (is_ovpg) {
		q->curpage = getPage(ovflowFile(q->rel), q->curpageid);
	}
	else {
		q->curpage = getPage(dataFile(q->rel), q->curpageid);
	}
	
	if (pageOvflow(q->curpage) != NO_PAGE) {
		q->is_ovflow = 1;
	}
	else {
		q->is_ovflow = 0;
	}
	q->curtup = 0;
}

// take a query string (e.g. "1234,?,abc,?")
// set up a QueryRep object for the scan

Query startQuery(Reln r, char *q)
{	
	Query new = malloc(sizeof(struct QueryRep));
	assert(new != NULL);

	Count nvals = nattrs(r);
	ChVecItem *cv = chvec(r);
	char **vals = malloc(nvals*sizeof(char *));
	assert(vals != NULL);
	tupleVals(q, vals);
	int i, j, k;
	Count rdepth = depth(r);
	rdepth = splitp(r) == 0 ? rdepth : rdepth + 1;
	Count rpage = npages(r);
	Bool *starBits = (Bool *)malloc(rdepth*sizeof(Bool));
	assert(starBits != NULL);
	int nstars = 0;
	memset(starBits, FALSE, rdepth*sizeof(Bool));
	for (i = 0; i < rdepth; i++) {
		Byte attidx = cv[i].att;
		if (strcmp(vals[attidx], "?") == 0) {
			starBits[i] = TRUE;
			nstars++;
		}
	}

	// calculate all possible page
	int allHashNum = (nstars < 1) ? 1 : (1 << nstars);
	Bits *allPossibleHash = (Bits *)malloc(allHashNum*sizeof(Bits));
	assert(allPossibleHash != NULL);
	memset(allPossibleHash, 0, allHashNum*sizeof(Bits));
	int set0and1Cnt = 0;
	for (i = 0; i < rdepth; i++) {
		if (starBits[i] == TRUE) {
			for (k = 0; k < allHashNum; k+=(allHashNum >> set0and1Cnt)) {
				for (j = 0; j < (allHashNum >> (set0and1Cnt + 1)); j++) {
					allPossibleHash[k+j] = setBit(allPossibleHash[k+j], i);
				}
			}
			set0and1Cnt++;
		}
		else {
			Byte attidx = cv[i].att;
			Byte bitidx = cv[i].bit;
			Bits hash = hash_any((unsigned char *)vals[attidx], strlen(vals[attidx]));
			if (bitIsSet(hash, bitidx)) {
				for (j = 0; j < allHashNum; j++) {
					allPossibleHash[j] = setBit(allPossibleHash[j], i);
				}
			}
		}
	}

	new->rel = r;
	new->search_str = q;
	new->curpage_idx = 0;
	new->pagenum = allHashNum;
	for (i = 0; i < allHashNum; i++) {
		if (getLower(allPossibleHash[i], rdepth) >= rpage) { // rpage start from 1, pageid start from 0
			new->pagenum--;
		}
	}
	new->all_possible_page = (PageID *)malloc(new->pagenum*sizeof(PageID));
	assert(new->all_possible_page != NULL);
	for (i = 0, j = 0; i < new->pagenum; i++, j++) {
		while (getLower(allPossibleHash[j++], rdepth) >= rpage)
			;
		
		new->all_possible_page[i] = getLower(allPossibleHash[--j], rdepth);
		// printf("may hash: %d\n", new->all_possible_page[i]);
	}
	new->curpageid = new->all_possible_page[new->curpage_idx];
	setQueryPageInfo(new, FALSE);

	freeVals(vals, nvals);
	free(vals);
	free(starBits);
	free(allPossibleHash);
	return new;
}

// get next tuple during a scan

Tuple getNextTuple(Query q)
{
	Reln r = q->rel;
	Page p = q->curpage;
	
	char *c = pageData(p) + q->curtup;
	Tuple cur_tuple = c; // 0x00 for spliting tuples in bucket
	Count cur_tuple_len = strlen(cur_tuple);

	while (PAGESIZE-(2*sizeof(Offset)+sizeof(Count))-q->curtup > pageFreeSpace(p)) {
		cur_tuple = c;
		cur_tuple_len = strlen(cur_tuple);
		q->curtup += cur_tuple_len+1;
		c += cur_tuple_len+1;
		if (tupleMatch(r, q->search_str, cur_tuple) == TRUE) {
			return cur_tuple;
		}
	}

	if (q->is_ovflow != 1) {
		q->curpage_idx++;
		if (q->curpage_idx < q->pagenum) {
			q->curpageid = q->all_possible_page[q->curpage_idx];
			free(q->curpage);
			setQueryPageInfo(q, FALSE);
			return getNextTuple(q);
		}
		else {
			return NULL;
		}
	}
	else {
		q->curpageid =  pageOvflow(q->curpage);
		free(q->curpage);
		setQueryPageInfo(q, TRUE);
		return getNextTuple(q);
	}
	return NULL;
}

// clean up a QueryRep object and associated data

void closeQuery(Query q)
{
	free(q->curpage);
	free(q->all_possible_page);
}
