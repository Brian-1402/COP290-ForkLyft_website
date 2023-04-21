default: run

run: run_local

test: test_report_html


run_local:
	flask --app forklyft_app --debug run

run_public:
	flask --app forklyft_app run --host=0.0.0.0

test_init:
	coverage run -m pytest
	coverage report
	# python3 -m pytest --cov=forklyft_app

test_report_html: test_init
	rm -rf coverage_report
	coverage html
	rm -f .coverage
	rm -f **/.coverage
	rm -rf .pytest_cache
	rm -rf **/.pytest_cache
	rm -rf tests/**/__pycache__

test_report_txt: test_init
	rm -f coverage_report.txt
	coverage report > coverage_report.txt
	rm -f .coverage
	rm -f **/.coverage
	rm -rf .pytest_cache
	rm -rf **/.pytest_cache
	rm -rf tests/**/__pycache__


clean:
	rm -rf tests/**/__pycache__
	rm -rf forklyft_app/**/__pycache__
	rm -f .coverage
	rm -f **/.coverage
	rm -rf .pytest_cache
	rm -rf **/.pytest_cache
	# rm -rf coverage_report
	# rm -f coverage_report.txt





