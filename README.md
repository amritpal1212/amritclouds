# CloudSync - Advanced File Cloud Storage

A modern file storage solution built with Firebase and Express.js, providing a user-friendly interface for file management.

## Project Structure

```
cloudsync/
├── public/                 # Frontend static files
│   ├── index.html         # Main HTML file
│   ├── app.js            # Frontend JavaScript
│   ├── config.js         # API configuration
│   └── styles.css        # Compiled Tailwind CSS
│
├── functions/             # Backend Firebase Functions
│   ├── index.js          # Main backend logic
│   └── package.json      # Backend dependencies
│
├── src/                   # Source files
│   └── input.css         # Tailwind CSS source
│
├── package.json          # Frontend dependencies
├── tailwind.config.js    # Tailwind CSS configuration
└── README.md            # Project documentation
```

## Features

- 🚀 Modern UI with Tailwind CSS
- 📤 Drag & Drop file upload
- 📥 Easy file download
- 🔍 File search functionality
- 📊 Storage statistics
- 📱 Responsive design
- 🔒 Secure file handling
- ⚡ Fast performance

## Tech Stack

### Frontend
- HTML5
- Tailwind CSS
- JavaScript (ES6+)
- Firebase Hosting

### Backend
- Firebase Functions
- Express.js
- Multer (File handling)
- CORS enabled

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cloudsync
   ```

2. **Install Frontend Dependencies**
   ```bash
   npm install
   ```

3. **Install Backend Dependencies**
   ```bash
   cd functions
   npm install
   ```

4. **Build Tailwind CSS**
   ```bash
   npm run build:css
   ```

5. **Firebase Setup**
   ```bash
   # Install Firebase CLI
   npm install -g firebase-tools

   # Login to Firebase
   firebase login

   # Initialize Firebase (select Hosting and Functions)
   firebase init
   ```

6. **Deploy to Firebase**
   ```bash
   # Deploy everything at once
   firebase deploy

   # Or deploy specific parts
   firebase deploy --only hosting    # Frontend only
   firebase deploy --only functions  # Backend only
   ```

## API Endpoints

### Files
- `GET /api/files` - List all files
- `POST /api/upload` - Upload files
- `GET /api/download/:fileId` - Download a file
- `DELETE /api/files/:fileId` - Delete a file

### Storage
- `GET /api/storage` - Get storage information

## Configuration

### Frontend Configuration
Edit `public/config.js`:
```javascript
const config = {
    apiUrl: '/api'  // Relative path for Firebase hosting
};
```

### Backend Configuration
The backend is configured in `functions/index.js` with:
- CORS settings for Firebase hosting
- File upload handling
- Storage limits
- API routes

## Development

1. **Start Frontend Development**
   ```bash
   npm run watch:css
   ```

2. **Start Backend Development**
   ```bash
   cd functions
   npm run serve
   ```

## Deployment

1. **Initial Firebase Setup**
   ```bash
   # Install Firebase CLI
   npm install -g firebase-tools

   # Login to Firebase
   firebase login

   # Initialize Firebase (select Hosting and Functions)
   firebase init
   ```

2. **Deploy Both Frontend and Backend**
   ```bash
   # Deploy everything at once
   firebase deploy

   # Or deploy specific parts
   firebase deploy --only hosting    # Frontend only
   firebase deploy --only functions  # Backend only
   ```

3. **Verify Deployment**
   - Frontend will be available at: `https://amritclouds.web.app`
   - API endpoints will be available at: `https://amritclouds.web.app/api/*`
   - No need to run the server locally after deployment

## Features in Detail

### File Management
- Multiple file upload
- Progress tracking
- File type detection
- Size limits
- Secure storage

### User Interface
- Modern design
- Responsive layout
- Dark mode
- Loading states
- Error handling

### Security
- CORS protection
- File validation
- Secure file storage
- Error handling

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email [your-email] or create an issue in the repository. 