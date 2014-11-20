@rem SET BRANCH=jp2014.2
SET BRANCH=jp2014.4
git push origin %BRANCH% --tags
git push sfjp %BRANCH% --tags
git push gh %BRANCH% --tags
