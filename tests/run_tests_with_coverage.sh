#!/bin/bash
# Clean previous coverage data
NAME=$(basename $(realpath .))
DOCS=/tmp/"$NAME"_coverage
export COVERAGE_FILE=/tmp/."$NAME"_coverage
echo @@ [$NAME] $DOCS $COVERAGE_FILE
rm -f "$COVERAGE_FILE"*
rm -rf $DOCS

# Run tests with coverage
python -m pytest tests/ \
  --cov=$NAME \
  --cov-append \
  --cov-report=term-missing || exit 1

echo @@ Combine all coverage data $COVERAGE_FILE
python -m coverage combine

echo @@ Generate HTML report in $DOCS
python -m coverage html \
  --directory="$DOCS" \
  --title="$NAME Coverage Report"

echo @@ "Coverage report generated at: $DOCS/index.html"