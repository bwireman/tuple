package tests

import (
	"testing"

	pilot "github.com/bwireman/tuple/pilot/pkg"
	test_util "github.com/bwireman/tuple/pilot/tests/test_util"
)

func Test_Container_JSONTags(t *testing.T) {
	test_util.ValidateTags(t, pilot.Container{})
}