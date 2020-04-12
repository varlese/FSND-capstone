curl --request POST \
  --url https://dev-j30osbgf.auth0.com/oauth/token \
  --header 'content-type: application/json' \
  --data '{"client_id":"8fMhWmn1ajthUKZI0DgIN7yEjXMoKU5x","client_secret":"uBgvAzu4z4qtXN9eu8g-SrlSf-JSLZhR6CSvbSXTdk9neA028QEjFhdosk7ZgNge","audience":"agency_dev","grant_type":"client_credentials"}'

export DOMAIN="https://dev-j30osbgf.auth0.com"
export CLIENT_ID="8fMhWmn1ajthUKZI0DgIN7yEjXMoKU5x"
export CLIENT_SECRET="uBgvAzu4z4qtXN9eu8g-SrlSf-JSLZhR6CSvbSXTdk9neA028QEjFhdosk7ZgNge"