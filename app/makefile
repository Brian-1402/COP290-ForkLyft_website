default: run

run: run_local

test: test_report_html


run_local:
	flask --app forklyft_app --debug run

run_public:
	flask --app forklyft_app run --host=0.0.0.0

test_init:
	coverage run -m pytest --junitxml=test_results/junit.xml
	coverage report

test_report_html: test_init
	rm -rf coverage_report
	coverage html
	rm -f .coverage
	rm -f **/.coverage
	rm -rf .pytest_cache
	rm -rf **/.pytest_cache
	rm -rf tests/__pycache__

test_report_txt: test_init
	rm -f coverage_report.txt
	coverage report > coverage_report.txt
	rm -f .coverage
	rm -f **/.coverage
	rm -rf .pytest_cache
	rm -rf **/.pytest_cache
	rm -rf tests/__pycache__

test_full_txt:
	coverage run -m pytest > test_output.txt
	coverage report > test_output_coverage.txt


clean:
	rm -rf tests/__pycache__
	rm -rf tests/**/__pycache__
	rm -rf seed_db/__pycache__
	rm -rf seed_db/**/__pycache__
	rm -rf forklyft_app/__pycache__
	rm -rf forklyft_app/**/__pycache__
	rm -f .coverage
	rm -f **/.coverage
	rm -rf .pytest_cache
	rm -rf **/.pytest_cache
	# rm -rf coverage_report
	# rm -f coverage_report.txt





