package handler

import (
	"regexp"
)

func getIdFromLink(link string) (string, bool) {
	re, _ := regexp.Compile(`(?:v=|\/)([0-9A-Za-z_-]{11}).*`)
	matches := re.FindStringSubmatch(link)
	if len(matches) >= 2 {
		return matches[1], true
	}
	return "", false
}
