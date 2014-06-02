@rem SET BRANCH=jp2014.2
SET BRANCH=jpbranch
git push sfjp %BRANCH% --tags
git push github %BRANCH% --tags
git push bb %BRANCH% --tags
