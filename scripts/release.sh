#!/bin/bash

set -x
set -e

release_type=${1}

version=$(./scripts/version.py get)
version_file=VERSION

commit=${BITBUCKET_COMMIT:-$(git rev-parse HEAD)}
branch=${ALLOWED_RELEASE_BRANCH:-master}

if ! git branch -a --contains "${commit}" | grep -e "^[* ]*remotes/origin/${branch}\$"
then
  echo -e "###\n### Not on ${branch}. Only ${branch} commits can be released.\n###"
  exit 1
else
  echo -e "###\n### Releasing of ${commit} on ${branch}\n###"
fi

# Do some release stuff here
# Publish docker image or copy to S3 bucket or whatever you need

git config user.name "Elon Musk"
git config user.email "elon.musk@spacex.com"

echo "Pushing detached tag of new version"
git add ${version_file}
git commit -m "Release version ${version}"
git tag  -a ${version} -m "Release version ${version} tag"
git push origin ${version}

echo "Pushing new version to ${branch}"
git fetch origin "${branch}:${branch}" || git pull
git checkout "${branch}"
./scripts/version.py inc-${release_type}

next_working_version=$(./scripts/version.py get --with-pre-release-placeholder)
git add ${version_file}
git commit -m "Incrementing working version to ${next_working_version} after ${version} release."
git push origin ${branch}
