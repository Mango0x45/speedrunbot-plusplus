/*
 * This file contains all sorts of utility functions and variables that are used throughout the
 * programs in this directory.
 */

#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <curl/curl.h>

#include "srcom/utils.h"

void *
xmalloc(const size_t size)
{
	void *ptr = malloc(size);
	if (ptr == NULL) {
		fputs("Error: Memory allocation error, the bot is likely out of RAM, try again "
		      "later.\n",
		      stderr);
		exit(EXIT_FAILURE);
	}
	return ptr;
}

void *
xrealloc(void *ptr, const size_t size)
{
	ptr = realloc(ptr, size);
	if (ptr == NULL) {
		fputs("Error: Memory reallocation error, the bot is likely out of RAM, try again "
		      "later.\n",
		      stderr);
		exit(EXIT_FAILURE);
	}
	return ptr;
}

void
init_string(string_t *str)
{
	str->len = 0;
	str->ptr = xmalloc(str->len + 1);
	str->ptr[0] = '\0';
}

struct game_t *
get_game(const char *abbrev)
{
	/* 52 is space for the rest of the URL */
	char *uri = xmalloc((strlen(abbrev) + 52) * sizeof(char));
	struct game_t *game = xmalloc(sizeof(struct game_t));
	string_t json;
	init_string(&json);

	sprintf(uri, API "/games?abbreviation=%s", abbrev);
	get_req(uri, &json);

	sscanf(json.ptr, "{\"data\":[{\"id\":\"%[^\"]\",\"names\":{\"international\":\"%[^\"]",
	       game->id, game->name);

	free(uri);
	free(json.ptr);
	if (game->id[0] == '\0')
		return NULL;
	return game;
}

char *
get_uid(const char *username)
{
	/* 46 is space for the rest of the URL */
	char *uri = xmalloc((strlen(username) + 46) * sizeof(char));
	string_t user;
	init_string(&user);

	sprintf(uri, API "/users?lookup=%s", username);
	get_req(uri, &user);

	static char uid[ID_LEN + 1];
	sscanf(user.ptr, "{\"data\":[{\"id\":\"%[^\"]", uid);

	free(uri);
	free(user.ptr);
	if (uid[0] == '\0')
		return NULL;
	return uid;
}

size_t
write_callback(const void *ptr, const size_t size, const size_t nmemb, string_t *json)
{
	/* Update the length of the JSON, and allocate more memory if needed. */
	const size_t new_len = json->len + size * nmemb;
	json->ptr = xrealloc(json->ptr, new_len + 1);

	/* Copy the incoming bytes to `json`. */
	memcpy(json->ptr + json->len, ptr, size * nmemb);
	json->ptr[new_len] = '\0';
	json->len = new_len;

	return size * nmemb;
}

void
get_req(const char *uri, string_t *json)
{
	CURL *curl = curl_easy_init();
	if (curl == NULL) {
		fputs("Error: Unable to initialize curl.\n", stderr);
		exit(EXIT_FAILURE);
	}

	/* Load the contents of the API request to `json`. */
	curl_easy_setopt(curl, CURLOPT_URL, uri);
	curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
	curl_easy_setopt(curl, CURLOPT_WRITEDATA, json);
	curl_easy_setopt(curl, CURLOPT_FAILONERROR, 1);

	CURLcode res;
rate_limit:
	if ((res = curl_easy_perform(curl)) != CURLE_OK) {
		if (res == RATE_LIMIT) {
			sleep(5);
			goto rate_limit;
		}

		curl_easy_cleanup(curl);
		fputs("Error: Unable to retrieve data from the sr.c API.\n", stderr);
		exit(EXIT_FAILURE);
	}

	curl_easy_cleanup(curl);
}

unsigned int
count_substr(const char *str, const char *const sub, const int subl)
{
	unsigned int c = 0;
	str = strstr(str, sub);
	while (str) {
		c++;
		str = strstr(str + subl, sub);
	}
	return c;
}

const char *
last_substr(const char *str, const char *const sub, const int subl)
{
	const char *ptr = strstr(str, sub);
	while (str) {
		ptr = str;
		str = strstr(str + subl, sub);
	}
	return ptr;
}
