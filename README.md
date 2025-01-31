# Web App - Books Available in SG Libraries (NLB)

This is the repository for a side project, [SGLibReads](https://sg-nlb-available-books.onrender.com/), which is a free web app for Singapore residents to search, save and more easily view the availability of Singapore library books. If you are a heavy user of the Singapore libraries, consider giving this web app a try.

## Tell Me Why?

### Why One - Providing a better way to search for NLB books

As of 2023, both the Singapore National Library Board's (NLB) app and website are great and functional. However, I found it difficult to save and search for book availability on their app and website. Wanting an easier way to hunt down the library books, I hacked out a rudimentary technical solution for my own personal use. As the stars started to align, and I learned more technical skills, thanks to NLB and the NLB Udemy Biz account no less, I realised I could develop a solution for the general Singapore public too. I hope to create value for the Singapore public, using skills I learned from public funds.

### Why Two - Changing SG government tech culture

When I learned about the [NLB public APIs](https://www.nlb.gov.sg/main/partner-us/contribute-and-create-with-us/NLBLabs), I realise I could use it for this side project. Unfortunately, the NLB API has so far provided a rather subpar developer experience (see my review [here](https://medium.com/@cliffy-gardens/how-good-is-our-latest-singapore-library-apis-an-honest-review-c32b03e8299b)). Nonetheless, I do feel this is also a chance to start more conversations on how some of our government agencies are running their tech deployments. I know there are competent government agencies running excellent tech solutions for Singapore too, and I hope this side project can do its part to contribute to the further strengthening of the Singapore technical core. Those interested in this conversation can follow me on [Medium](https://medium.com/@cliffy-gardens), or add me on [LinkedIn](https://www.linkedin.com/in/cliff-chew-kt/).

### Why Three - Adding more technical skills

This side project is also a way for me to continue to learn and apply more technical skills into a reasonably real-world setting. Some of the possible features I hope to learn and include into this web app includes:

1. Availability of eBooks
2. Linking to NLB Events from EventBrite
3. Recommending books

## Getting Started

The following section details the setup steps and development workflow for this web-app.

### Prerequisites

Development:

- Node.js and npm (for frontend)
- Python 3.11+ (for backend)
- Supabase CLI
- Docker (for Supabase)

Deployment:

- Firebase CLI
- Google Cloud CLI

### 1. Setup Steps

#### 1.1 Supabase Setup

The [Supabase CLI](https://supabase.io/docs/guides/cli) is required to manage
 the database schema and seed data. Please follow the instructions below:

1. Install Supabase CLI using the official guide [here](https://supabase.com/docs/guides/cli/getting-started#installing-the-supabase-cli).

1. Authenticate Supabase CLI with the following command:

    ```bash
    supabase login
    ```

1. Start the local Supabase instance:

    ```bash
    supabase start
    ```

##### Google Auth Setup

Only works on managed supabase instances at supabase.com

1. Create a supabase project and go to `Authentication` -> `Providers`, and enable Google Auth. Copy the callback URL.

1. Go to `Project Settings` and note down your supabase project ID.

1. Go to [Google Cloud Console](https://console.cloud.google.com) and create a new project.

1. Navigate to `APIs & Services` -> `Library`, search for `Identity Toolkit API` and enable it.

1. Go to `APIs & Services` -> `Credentials`.

1. Click `Create Credentials` -> `OAuth 2.0 Client ID`.

1. Configure your consent screen. Then go back to `APIs & Services` -> `Credentials` + `Create Credentials` -> `OAuth 2.0 Client ID` and refresh the page.

1. Select `Web Application` as the type.

1. Add the following URLs under `Authorized Redirect URIs`: `http://localhost:54321/auth/v1/callback` and the callback URL you copied in step 1.

1. Click `Create`.

    In the project root folder, run

    ```bash
    supabase link --project-ref '<PROJECT_ID>' # From Supabase Project Settings page
    supabase db push
    ```

#### 1.2 Back-end FastAPI Server Setup

1. Navigate to back-end directory:

    ```bash
    cd back-end
    ```

1. Install `uv` in your local machine. Please follow the
 [official guide](https://docs.astral.sh/uv/getting-started/installation/)
 for more information.

1. Copy the example environment file:.

    ```bash
    cp --update=none .env.example .env
    ```

1. Update the .env file with the Supabase API credentials and NLB Catalogue API credentials. For Supabase API credentials, you can view them via the Supabase dashboard under `Configuration` -> `API`. For NLB Catalogue API credentials, you will need to make a separate request for API access via [this form](https://www.nlb.gov.sg/main/partner-us/contribute-and-create-with-us/NLBLabs).

#### 1.3 Front-end Svelte Setup

1. Navigate to front-end directory:

    ```bash
    cd front-end
    ```

1. Copy the example environment file. Update your Supabase anon key accordingly. You can view them via the Supabase dashboard under `Configuration` -> `API`.

    ```bash
    cp --update=none .env.example .env
    ```

1. Install dependencies with npm.

    ```bash
    npm install
    ```

### 2. Development Workflow

1. From project root folder, start-up Supabase server with supabase-cli.

    ```bash
    supabase start
    ```

1. Run Backend (FastAPI)

    ```bash
    cd back-end
    uv run -- uvicorn src.main:app --reload
    ```

1. Run Frontend (Svelte)

    ```bash
    cd front-end # Run this in a separate terminal from the backend.
    npm run dev -- --open
    ```

### 3. Building and Deploying for Production

1. Backend Deployment to Google Artifact Registry

    - Automated CI/CD pipeline triggers on push to main branch
    - Builds Docker image
    - Pushes to Google Artifact Registry
    - Deploys to specified Google Cloud Run for managed container service.

2. Frontend Deployment to Firebase Hosting

    - Automated CI/CD pipeline triggers on push to main branch
    - Builds Svelte application
    - Deploys to Firebase Hosting

### Code Linting and Formatting

For code linting and formatting, this project uses [ruff](https://github.com/astral-sh/ruff) for Python, and [prettier](https://prettier.io) for Typescript.

To integrate this seamlessly to your development workflow, we recommend
using [pre-commit](https://pre-commit.com/) to run the formatter and linter before
committing to the repository.

From the project root folder.

1. Set up the git hook scripts

    ```bash
    pre-commit install
    ```

    You should see the message `pre-commit installed at .git/hooks/pre-commit`.

2. Run `git commit` as usual to commit your changes.
