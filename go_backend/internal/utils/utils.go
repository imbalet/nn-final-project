package utils

import (
	"fmt"
	"reflect"
)

func GetStructFields(s interface{}, tagName string) ([]string, []interface{}, error) {
	val := reflect.ValueOf(s)
	typ := val.Type()

	if typ.Kind() != reflect.Struct {
		return nil, nil, fmt.Errorf("passed object is not a struct")
	}

	var tags []string
	var values []interface{}

	for i := 0; i < typ.NumField(); i++ {
		field := typ.Field(i)
		value := val.Field(i)

		if !field.IsExported() {
			continue
		}

		tag := field.Tag.Get(tagName)
		if tag == "" {
			tag = field.Name
		}

		tags = append(tags, tag)
		values = append(values, value.Interface())
	}

	return tags, values, nil
}
