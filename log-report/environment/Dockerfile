# Pin the base image by digest so the build is reproducible.
# Approved base: python:3.11-slim (SHA256 pinned below)
FROM python:3.11-slim@sha256:541fbb78d73882c9b3ca6c90b9e2d84ccc893f36ecca10b31c13b86b69e78ea7

# Install verifier dependencies so test.sh never calls pip at verify time.
RUN pip install --no-cache-dir pytest pytest-json-ctrf

# Prepare the working directory for the agent.
WORKDIR /app

# Copy only the access log (the input data). Do NOT copy solution files.
COPY data/access.log /app/access.log

# NOTE: solution/solve.sh was removed from the build context.
# It must NOT be copied here to avoid leaking the reference answer to the agent.
