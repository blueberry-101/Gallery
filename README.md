<p align="center">
  <img src="https://res.cloudinary.com/dmxd0zztv/image/upload/v1717149521/static_files_Gallery/instagram-logo2-removebg-preview_cyb9cc.png" width="100" />
</p>
<p align="center">
    <h1 align="center">GALLERY</h1>
</p>
<p align="center">
    <em>Not A Instagram Clone!</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/blueberry-101/Gallery?style=flat&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/blueberry-101/Gallery?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/blueberry-101/Gallery?style=flat&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/blueberry-101/Gallery?style=flat&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
		<em>Developed with the software and tools below.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/badge/HTML5-E34F26.svg?style=flat&logo=HTML5&logoColor=white" alt="HTML5">
	<img src="https://img.shields.io/badge/Cloudinary-3448C5?style=for-the-badge&logo=Cloudinary&logoColor=white" alt="Cloudinary">
	<img src="https://img.shields.io/badge/Railway-131415?style=for-the-badge&logo=railway&logoColor=white" alt="Railway.app">
	<img src="https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens" alt="JWT">
	<img src="https://img.shields.io/badge/Redis-DC382D.svg?style=flat&logo=Redis&logoColor=white" alt="Redis">
	<img src="https://img.shields.io/badge/YAML-CB171E.svg?style=flat&logo=YAML&logoColor=white" alt="YAML">
	<img src="https://img.shields.io/badge/Gunicorn-499848.svg?style=flat&logo=Gunicorn&logoColor=white" alt="Gunicorn">
	<br>
	<img src="https://img.shields.io/badge/Celery-37814A.svg?style=flat&logo=Celery&logoColor=white" alt="Celery">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat&logo=Docker&logoColor=white" alt="Docker">
	<img src="https://img.shields.io/badge/Django-092E20.svg?style=flat&logo=Django&logoColor=white" alt="Django">
</p>
<hr>


## Quick Links

> - [Overview](#overview)
> - [Features](#features)
> - [Fixes](#fixes)
> - [Contributing](#contributing)
> - [License](#license)

---

## Overview


#[Live Demo](https://whitegallery.up.railway.app/)


Gallery is a Django-based project designed to provide a comprehensive platform for managing and displaying images. The project features a robust backend for handling image uploads, storage, and retrieval, along with a clean and intuitive frontend interface for users.

<p align="center">
  <img src="https://github.com/blueberry-101/Gallery/blob/main/readmeassets/Screenshot%202024-05-31%20165656.jpg" alt="Screenshot 1" width="800" />
<img src="https://github.com/blueberry-101/Gallery/blob/main/readmeassets/Screenshot%202024-07-17%20015437.jpg" alt="Screenshot 6" width="800" />
  <img src="https://github.com/blueberry-101/Gallery/blob/main/readmeassets/Screenshot%202024-05-31%20165756.jpg" alt="Screenshot 2" width="800" />
  <img src="https://github.com/blueberry-101/Gallery/blob/main/readmeassets/Screenshot%202024-05-31%20165829.jpg" alt="Screenshot 3" width="800" />
  <img src="https://github.com/blueberry-101/Gallery/blob/main/readmeassets/Screenshot%202024-05-31%20170000.jpg" alt="Screenshot 4" width="800" />
  <img src="https://github.com/blueberry-101/Gallery/blob/main/readmeassets/Screenshot%202024-05-31%20170134.jpg" alt="Screenshot 5" width="800" />
  
</p>



---

## Features

1. **Validators**: Validate size and extension of posts. Ensure only valid image extensions are uploaded.
2. **Restrictions**: Implement three restrictions: (a) Prevent overpopulation of images, (b) Limit rapid image uploads, and (c) Enforce size limits on images. Additionally, implementing a delete feature will erase associated files permanently.
3. **Cloud Storage**: Moved from server-side storage to cloud storage using Cloudinary, providing scalable and reliable storage solutions.
4. **Background Processing**: Utilize Django-Celery as a background worker and Redis as a message broker for asynchronous processing. Implement a mail system on SignUp to Gallery, first post on Gallery, and reset password, using Celery to reduce response time in email and image post.
5. **Notifications**: Utilize the Messages Framework in Django to push toast notifications on various events such as image upload, image delete, and image size alerts.
6. **Model Relationship**: Include preupload images to get users started. Utilize Model Relationships to assign users with preuploaded images.
7. **Authentication using JWT**: Implement authentication using JSON Web Tokens (JWT) for SignUp and changing password token.

---

## Fixes

- **Upload Bar**: Add a upload bar for visulizing the image uploading.
- **Phone number**: Add a phone number verification service using twillio etc.
- **Improve Performance**: Optimize database queries and image processing for faster load times.
- **UI/UX Improvements**: Revamp the user interface for a more modern and user-friendly experience.

---

## Contributing

Contributions are welcome! Here are several ways you can contribute:

- **Submit Pull Requests**: Review open PRs, and submit your own PRs.
- **Join the Discussions**: Share your insights, provide feedback, or ask questions.
- **Report Issues**: Submit bugs found or log feature requests for Gallery.



1. **Fork the Repository**: Start by forking the project repository to your GitHub account.
2. **Clone Locally**: Clone the forked repository to your local machine using a Git client.
   ```sh
   git clone https://github.com/blueberry-101/Gallery
2. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x

2. **Make Your Changes**: Develop and test your changes locally.

2. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
2. **Push to GitHub**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
2. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.

*Once your PR is reviewed and approved, it will be merged into the main branch.*
