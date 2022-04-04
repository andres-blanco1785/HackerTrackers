# Running this web app locally
As of now, this application utilizes the [Solana Beach API](https://github.com/solana-beach/api). Once you generate your API key, you can paste it into the `.envCOPY` file and rename it to `.env` 
## Frontend
- If your terminal is not located in the "frontend" folder, use the command `cd frontend` and install the npm packages by running `npm install` or `npm i`
- once the packages are installed, you can run the development server with `npm run start`
## Backend
- Ensure that your terminal is in the root folder and run the command `flask run`
## API
- To receive a list of all blacklisted accounts, run "http://localhost:5000/blacklist/".
- To find if an account is blacklisted, run "http://localhost:5000/blacklisted/?account={account_signature}".
