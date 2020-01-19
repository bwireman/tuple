package test_util

import (
	"reflect"
	"testing"
	"strings"
)

func getTags(s interface{}) []string {
	tags := []string{}
	val := reflect.ValueOf(s)
	for i := 0; i < val.Type().NumField(); i++ {
		tags = append(tags, val.Type().Field(i).Tag.Get("json"))
	}
	return tags
}

func ValidateTags(t *testing.T, s interface{}) {
	tags := getTags(s)
	for _, tag := range tags {
		if tag != strings.ToLower(tag) {
			t.Error("JSON Tag: ", tag," was not snake_case")
		}
	}
}
