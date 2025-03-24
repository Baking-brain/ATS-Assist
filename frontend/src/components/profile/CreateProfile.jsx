import React, { useState } from "react";
import "./CreateProfile.css";

export default function ProfilePage() {
  const [profileImage, setProfileImage] = useState(null);
  const [formData, setFormData] = useState({
    name: "",
    domain: "",
    place: "",
    bio: "",
    email: "",
    phone: "",
  });

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        setProfileImage(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Form submitted:", formData);
    console.log("Profile image:", profileImage);
  };

  return (
    <div className="create-profile-container">
      <h1>Create Your Profile</h1>

      <form onSubmit={handleSubmit}>
        <div className="image-upload-container">
          <div
            className="image-preview"
            style={{
              backgroundImage: `url(${profileImage || "/default-avatar.png"})`,
            }}
          >
            {!profileImage && <span>+</span>}
          </div>
          <input
            type="file"
            id="profile-image"
            accept="image/*"
            onChange={handleImageChange}
            className="image-input"
          />
          <label htmlFor="profile-image" className="image-label">
            {profileImage ? "Change Photo" : "Upload Photo"}
          </label>
        </div>

        <div className="form-group">
          <label htmlFor="name">Full Name</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            placeholder="Enter your full name"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="domain">Domain/Profession</label>
          <input
            type="text"
            id="domain"
            name="domain"
            value={formData.domain}
            onChange={handleInputChange}
            placeholder="e.g. Software Engineer, Designer, etc."
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="place">Location</label>
          <input
            type="text"
            id="place"
            name="place"
            value={formData.place}
            onChange={handleInputChange}
            placeholder="City, Country"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleInputChange}
            placeholder="your.email@example.com"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="phone">Phone Number</label>
          <input
            type="tel"
            id="phone"
            name="phone"
            value={formData.phone}
            onChange={handleInputChange}
            placeholder="Your phone number"
          />
        </div>

        <div className="form-group">
          <label htmlFor="bio">Bio</label>
          <textarea
            id="bio"
            name="bio"
            value={formData.bio}
            onChange={handleInputChange}
            placeholder="Write a short bio about yourself"
            rows="4"
          />
        </div>

        <button type="submit" className="submit-button">
          Create Profile
        </button>
      </form>
    </div>
  );
}
