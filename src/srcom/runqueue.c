/*
 * This program gets the number of runs in the verification queue of a given game
 * (argv[1]).
 */

#include <pthread.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <jansson.h>

#include "srcom/runqueue.h"
#include "srcom/utils.h"

bool done = false;
char uri_base[URIBUF];
int offset_start = 0;
int fgcounts[THREAD_COUNT], ilcounts[THREAD_COUNT];

void usage(void)
{
	fputs("Usage: `+runqueue [PLAYER NAME]`\n"
	      "Example: `+runqueue AnInternetTroll`\n",
	      stderr);
	exit(EXIT_FAILURE);
}

void *routine(void *tnum)
{
	/* 
	 * Equivalant to `(int) tnum` but supresses compiler warnings that can
	 * be safely ignored. 
	 */
	int s, i_tnum = *((int *) &tnum);
	char uri[URIBUF], size[URIBUF];
	string_t json;

	/* Make a GET request. */
	snprintf(uri, URIBUF, "%s%d", uri_base,
	         offset_start + MAX_RECV * i_tnum);
	init_string(&json);
	get_req(uri, &json);

	char *size_key = last_substr(json.ptr, "\"size\":", 7);
	sscanf(size_key, "\"size\":%[^,]", size);

	if ((s = atoi(size)) < MAX_RECV)
		done = true;

	/* Loop through each pending run and tally the fullgame and IL runs. */
	json_t *root, *data, *obj, *level;
	json_error_t error;
	root = json_loads(json.ptr, 0, &error);
	if (!root) {
		fputs("Error: Unable to parse sr.c reponse, try again later.\n",
		      stderr);
		exit(EXIT_FAILURE);
	}
	data = json_object_get(root, "data");

	for (size_t i = 0, len = json_array_size(data); i < len; i++) {
		obj = json_array_get(data, i);
		level = json_object_get(obj, "level");

		if (level->type != JSON_NULL)
			ilcounts[i_tnum]++;
		else
			fgcounts[i_tnum]++;
	}

	json_decref(root);
	free(json.ptr);
	return NULL;
}

int main(int argc, char **argv)
{
	if (argc != 2)
		usage();

	string_t json;
	init_string(&json);

	/* Get the games ID and name. */
	char gid[UIDBUF], gname[BUFSIZ];
	snprintf(uri_base, URIBUF, API "/games?abbreviation=%s", argv[1]);
	get_req(uri_base, &json);

	sscanf(json.ptr,
	       "{\"data\":[{\"id\":\"%[^\"]\",\"names\":{\"international\":\"%["
	       "^\"]",
	       gid, gname);

	snprintf(uri_base, URIBUF,
	         API "/runs?game=%s&status=new&max=200&offset=", gid);

	while (!done) {
		pthread_t threads[THREAD_COUNT];
		for (int i = 0; i < THREAD_COUNT; i++) {
			/*
			* This cast is a could be replaced with a simple `(void *) i`
			* cast, but the compiler doesn't like it when I do that.
			*/
			if (pthread_create(&threads[i], NULL, &routine,
			                   *((void **) &i))
			    != 0) {
				fputs("Error: Failed to create thread.\n",
				      stderr);
				return EXIT_FAILURE;
			}
		}

		for (int i = 0; i < THREAD_COUNT; i++) {
			if (pthread_join(threads[i], NULL) != 0) {
				fputs("Error: Failed to join thread.\n",
				      stderr);
				return EXIT_FAILURE;
			}
		}

		offset_start += THREAD_COUNT * MAX_RECV;
	}

	int fullgame = 0, il = 0;
	for (int i = 0; i < THREAD_COUNT; i++) {
		fullgame += fgcounts[i];
		il += ilcounts[i];
	}

	printf("Runs Awaiting Verification: %s\n"
	       "Fullgame: %d\n"
	       "Individual Level: %d\n"
	       "Total: %d\n",
	       gname, fullgame, il, fullgame + il);
	return EXIT_SUCCESS;
}