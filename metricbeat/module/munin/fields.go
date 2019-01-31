// Licensed to Elasticsearch B.V. under one or more contributor
// license agreements. See the NOTICE file distributed with
// this work for additional information regarding copyright
// ownership. Elasticsearch B.V. licenses this file to you under
// the Apache License, Version 2.0 (the "License"); you may
// not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.

// Code generated by beats/dev-tools/cmd/asset/asset.go - DO NOT EDIT.

package munin

import (
	"github.com/elastic/beats/libbeat/asset"
)

func init() {
	if err := asset.SetFields("metricbeat", "munin", asset.ModuleFieldsPri, AssetMunin); err != nil {
		panic(err)
	}
}

// AssetMunin returns asset data.
// This is the base64 encoded gzipped contents of ../metricbeat/module/munin.
func AssetMunin() string {
	return "eJx8kU1qwzAUhPc+xZBNIBAfQIveoL1CkK2Jq0Z/SM+0vn2xpZaYmi7fzBvm09MVDy4Kfg42dIBYcVQ4va7zqQMMy5htEhuDwksHAJuHEA3hKdmOBfxKMQtzB2Q66kKFgaI74G7pTFFb8oqgPVtb38L9ZfMAWRIV4vDBUZpUh1t1TJwHx7/OzeuUbJja2vlybjsH7Bv/E3ShwbBAI7l5sgHxDl3x6gP1xCD9AXzd71dph//g8hmz+Z/gTXuuVfLOn+IxOsdRbJhWtfye9qB71zflOKemPJ+6pvaf8R0AAP//7IiXDQ=="
}