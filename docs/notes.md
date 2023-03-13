# size

The metadata for each project (repo) has useful statistics about repo size and storage size:

```
curl https://renkulab.io/knowledge-graph/projects/omnibenchmark/omni-batch-py/csf-patients-py/ | jq

{
  "version": "9",
  "_links": [
    {
      "rel": "self",
      "href": "https://renkulab.io/knowledge-graph/projects/omnibenchmark/omni-batch-py/csf-patients-py"
    },
    {
      "rel": "datasets",
      "href": "https://renkulab.io/knowledge-graph/projects/omnibenchmark/omni-batch-py/csf-patients-py/datasets"
    }
  ],
  "identifier": 19665,
  "path": "omnibenchmark/omni-batch-py/csf-patients-py",
  "name": "csf_patients_py",
  "visibility": "public",
  "created": {
    "creator": {
      "email": "almut.lue@gmail.com",
      "name": "Almut Luetge"
    },
    "dateCreated": "2022-06-29T10:52:50Z"
  },
  "updatedAt": "2022-12-08T11:02:04.560Z",
  "urls": {
    "readme": "https://renkulab.io/gitlab/omnibenchmark/omni-batch-py/csf-patients-py/-/blob/master/README.md",
    "ssh": "git@renkulab.io:omnibenchmark/omni-batch-py/csf-patients-py.git",
    "http": "https://renkulab.io/gitlab/omnibenchmark/omni-batch-py/csf-patients-py.git",
    "web": "https://renkulab.io/gitlab/omnibenchmark/omni-batch-py/csf-patients-py"
  },
  "forking": {
    "forksCount": 0
  },
  "keywords": [],
  "starsCount": 0,
  "permissions": {
    "projectAccess": {
      "level": {
        "name": "Maintainer",
        "value": 40
      }
    }
  },
  "images": [],
  "statistics": {
    "commitsCount": 32,
    "storageSize": 13960979,
    "repositorySize": 314572,
    "lfsObjectsSize": 7161688,
    "jobArtifactsSize": 6484719
  }
}
```


## git-lfs usage (checking out single files)

You can specify the --include or -I flag (they are aliases of each other) to only include a specific filename in your pull.

For example, if you only wanted to pull the file called "a.dat", try:

$ git lfs pull --include "a.dat"

Or, if you only wanted to pull files matching the ".dat" extension, try:

$ git lfs pull --include "*.dat"

## python package

* See: https://pypi.org/project/git-lfs/
* Useful to avoid external dependency towards the git-lfs binary (but check maturity/performance).
