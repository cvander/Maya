FROM python:3.14-slim

WORKDIR /app

RUN pip install --no-cache-dir pytest pyyaml

# Copy only what's needed (no .env, no secrets)
COPY skills/ skills/
COPY docs/ docs/
COPY data/ data/
COPY maya/ maya/
COPY evals/ evals/
COPY tests/ tests/
COPY CLAUDE.md AGENTS.md SOUL.md ./

# Verify the skill system works
RUN python -c "import skills._lib.runner; import skills._lib.io; import skills._lib.md_table; print('Imports OK')"

# Default: run all tests
CMD ["python", "-m", "pytest", \
     "skills/inventory_check/test_main.py", \
     "skills/vendor_order_review/test_main.py", \
     "skills/vendor_order/test_main.py", \
     "skills/vendor_contact/test_main.py", \
     "skills/schedule_view/test_main.py", \
     "skills/schedule_draft/test_main.py", \
     "skills/schedule_notify/test_main.py", \
     "skills/close_out/test_main.py", \
     "skills/close_out_report/test_main.py", \
     "skills/cost_analysis/test_main.py", \
     "skills/eighty_six/test_main.py", \
     "skills/compliance_check/test_main.py", \
     "skills/compliance_docs/test_main.py", \
     "skills/music_book/test_main.py", \
     "skills/music_calendar/test_main.py", \
     "maya/seed/", \
     "maya/onboard/", \
     "evals/", \
     "tests/", \
     "-v", "--tb=short"]
