#!/bin/bash

git checkout archive-$(date +%F) || git checkout -b archive-$(date +%F)
git add *
git commit -m "archive"
git checkout main
