# Use the official Flutter image for building the app
FROM cirrusci/flutter:stable AS build

# Set the working directory
WORKDIR /app

# Copy pubspec.yaml and pubspec.lock to the container
COPY pubspec.yaml pubspec.lock ./

# Install dependencies
RUN flutter pub get

# Copy the rest of the project to the container
COPY . .

# Build the Flutter app for release
RUN flutter build apk --release

# Use a smaller image for serving the Flutter app
FROM nginx:alpine

# Copy the built app to the nginx html directory
COPY --from=build /app/build/app/outputs/flutter-apk/app-release.apk /usr/share/nginx/html/app-release.apk

# Expose port 80
EXPOSE 80
