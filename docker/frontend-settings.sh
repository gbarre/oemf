echo "Inject environment variables in main*.js files..."
for f in $(find /usr/share/nginx/html/ -maxdepth 1 -type f -name 'main*.js')
do
    sed -i \
        -e "s|__API_URL__|$API_URL|g" \
    "$f"
done
echo "Done."
