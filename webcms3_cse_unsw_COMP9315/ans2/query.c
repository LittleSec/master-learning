// query.c ... query scan functions
// part of Multi-attribute Linear-hashed Files
// Manage creating and using Query objects
// Last modified by John Shepherd, July 2019

#include "defs.h"
#include "query.h"
#include "reln.h"
#include "tuple.h"
#include "hash.h"
#include "bits.h"
#include "page.h"

// A suggestion ... you can change however you like

struct QueryRep {
	Reln    rel;       // need to remember Relation info
	PageID  curpageid; // current pageid in scan
	Page    curpage;   // current page in scan
	int     is_ovflow; // are we in the overflow pages?
	Offset  curtup;    // offset of current tuple within page
	Tuple   query_str; // need to remember query string
	PageID  *all_pos_pageid;
	Count   len_pid_arr; // len of all_pos_pageid
	Offset  curpage_idx; // idx for all_pos_pageid, idx < len
};

// buf no ' '(space), can't come from bitsString()
Bits str2Bits(char *buf)
{
	int i; Bits ret = 0;
	for (i = 0; i < strlen(buf); i++)
		if (buf[i] == '1') ret = setBit(ret, i);
	return ret;
}

void dfsCalAllPosHash(char *ma, Offset cur_ma_idx, char *ans, Bits *res_arr, Offset *cur_res_idx)
{
	if (strlen(ma) == cur_ma_idx) {
		res_arr[*cur_res_idx] = str2Bits(ans);
		*cur_res_idx += 1;
	}
	else {
		if (ma[cur_ma_idx] != '?') {
			ans[cur_ma_idx] = ma[cur_ma_idx];
			dfsCalAllPosHash(ma, cur_ma_idx+1, ans, res_arr, cur_res_idx);
		}
		else {
			ans[cur_ma_idx] = '0';
			dfsCalAllPosHash(ma, cur_ma_idx+1, ans, res_arr, cur_res_idx);
			ans[cur_ma_idx] = '1';
			dfsCalAllPosHash(ma, cur_ma_idx+1, ans, res_arr, cur_res_idx);
		}
	}
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
	int i, j;
	Count rdepth = depth(r);
	rdepth = splitp(r) == 0 ? rdepth : rdepth + 1;
	Count rpage = npages(r);

	// get all possible pages
	Count nqm = 0;
	char *haststr = (char *)malloc((rdepth+1)*sizeof(char)); // like 1??01
	haststr[rdepth] = '\0';
	for (i = 0; i < rdepth; i++) {
		Byte attidx = cv[i].att;
		if (strcmp(vals[attidx], "?") == 0) {
			haststr[i] = '?';
			nqm++;
		}
		else {
			Byte attidx = cv[i].att;
			Byte bitidx = cv[i].bit;
			Bits hash = hash_any((unsigned char *)vals[attidx], strlen(vals[attidx]));
			haststr[i] = bitIsSet(hash, bitidx) ? '1' : '0';
		}
	}
	int allHashNum = (nqm < 1) ? 1 : (1 << nqm);
	Bits *allPosHash = (Bits *)malloc(allHashNum*sizeof(Bits));
	assert(allPosHash != NULL);
	char *tmpstr = (char *)malloc((rdepth+1)*sizeof(char));
	tmpstr[rdepth] = '\0';
	Offset tmpidx = 0;
	dfsCalAllPosHash(haststr, 0, tmpstr, allPosHash, &tmpidx);
	free(tmpstr);

	new->rel = r;
	new->query_str = q;
	new->curpage_idx = 0;
	new->curtup = 0;
	new->len_pid_arr = allHashNum;
	for (i = 0; i < allHashNum; i++)
		if (allPosHash[i] >= rpage) new->len_pid_arr--;
	new->all_pos_pageid = (PageID *)malloc(new->len_pid_arr*sizeof(PageID));
	assert(new->all_pos_pageid != NULL);
	for (i = 0, j = 0; i < new->len_pid_arr; i++) {
		do {
			j++;
		} while (allPosHash[j] >= rpage) ;
		new->all_pos_pageid[i] = allPosHash[j];
	}
	new->curpageid = new->all_pos_pageid[0];
	new->curpage = getPage(dataFile(new->rel), new->curpageid);
	if (pageOvflow(new->curpage) != NO_PAGE) new->is_ovflow = 1;
	else new->is_ovflow = 0;

	freeVals(vals, nvals);
	free(vals);
	free(allPosHash);
	return new;
}

// get next tuple during a scan
Tuple getNextTuple(Query q)
{
	char *c = pageData(q->curpage) + q->curtup;
	Tuple cur_tuple = c;
	Count len_cur_tuple = strlen(cur_tuple);

	while (PAGESIZE-(2*sizeof(Offset)+sizeof(Count))-q->curtup > pageFreeSpace(q->curpage)) {
		cur_tuple = c;
		len_cur_tuple = strlen(cur_tuple);
		q->curtup += len_cur_tuple+1;
		c += len_cur_tuple+1;
		if (tupleMatch(q->rel, q->query_str, cur_tuple)) return cur_tuple;
	}

	if (q->is_ovflow == 1) { // search ovpage
		q->curpageid =  pageOvflow(q->curpage);
		free(q->curpage);
		q->curpage = getPage(ovflowFile(q->rel), q->curpageid);
		if (pageOvflow(q->curpage) != NO_PAGE) q->is_ovflow = 1;
		else q->is_ovflow = 0;
		q->curtup = 0;
		return getNextTuple(q);
	}
	else { // next page
		q->curpage_idx++;
		if (q->curpage_idx < q->len_pid_arr) {
			q->curpageid = q->all_pos_pageid[q->curpage_idx];
			free(q->curpage);
			q->curpage = getPage(dataFile(q->rel), q->curpageid);
			if (pageOvflow(q->curpage) != NO_PAGE) q->is_ovflow = 1;
			else q->is_ovflow = 0;
			q->curtup = 0;
			return getNextTuple(q);
		}
		else {
			return NULL;
		}
	}

	return NULL;
}

// clean up a QueryRep object and associated data
void closeQuery(Query q)
{
	free(q->curpage);
	free(q->all_pos_pageid);
}
