FROM python:3.13-alpine
LABEL maintainer="Mario Ramirez marm1984@gmail.com"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Install dependencies first
COPY ./requirements.txt /requirements.txt
COPY ./requirements.dev.txt /requirements.dev.txt

ARG DEV=0
# psycopg[binary] ships prebuilt wheels, so no compiler or libpq headers are needed.
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    /py/bin/pip install -r /requirements.txt && \
    if [ "$DEV" = "1" ]; then /py/bin/pip install -r /requirements.dev.txt; fi

# Create unprivileged user
RUN adduser \
    --disabled-password \
    --no-create-home \
    mario-user

# Copy project files and the run script
COPY ./manage.py /app/manage.py
COPY ./mario_portfolio /app/mario_portfolio/
COPY ./portfolio /app/portfolio/
COPY ./scripts /scripts/

# Static files only change with the code, so collect them once at build time
# instead of on every container start. They go to /vol/static (STATIC_ROOT),
# outside /app, so the dev bind mount over /app doesn't hide them.
RUN /py/bin/python /app/manage.py collectstatic --noinput && \
    chmod +x /scripts/run.sh && \
    chmod -R 755 /scripts /app && \
    chown -R mario-user:mario-user /app /vol

WORKDIR /app

# Add scripts directory and venv to PATH
ENV PATH="/scripts:/py/bin:$PATH"

USER mario-user

CMD ["/scripts/run.sh"]