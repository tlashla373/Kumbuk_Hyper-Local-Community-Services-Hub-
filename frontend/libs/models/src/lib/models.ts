// Core types for Kumbuk application

export interface User {
  id: string;
  email: string;
  userType: 'consumer' | 'provider' | 'admin';
  profile: UserProfile;
  createdAt: Date;
  updatedAt: Date;
}

export interface UserProfile {
  firstName: string;
  lastName: string;
  phoneNumber?: string;
  location?: Location;
  preferences?: UserPreferences;
}

export interface UserPreferences {
  language: 'en' | 'si' | 'ta';
  notifications: NotificationSettings;
  theme: 'light' | 'dark' | 'auto';
}

export interface NotificationSettings {
  push: boolean;
  email: boolean;
  sms: boolean;
}

export interface Location {
  id: string;
  name: string;
  district: string;
  province: string;
  coordinates?: {
    latitude: number;
    longitude: number;
  };
}

export interface ServiceProvider {
  id: string;
  userId: string;
  businessName: string;
  description: string;
  contactInfo: ContactInfo;
  serviceCategories: ServiceCategory[];
  location: Location;
  verificationStatus: 'pending' | 'verified' | 'rejected';
  rating?: number;
  totalReviews?: number;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface ContactInfo {
  phoneNumber: string;
  whatsAppNumber?: string;
  email?: string;
  address?: string;
  website?: string;
}

export interface ServiceCategory {
  id: string;
  name: string;
  description: string;
  icon?: string;
  parentCategoryId?: string;
}

export interface Inquiry {
  id: string;
  consumerId: string;
  providerId: string;
  message: string;
  status: 'sent' | 'read' | 'responded' | 'closed';
  response?: string;
  createdAt: Date;
  respondedAt?: Date;
}

export interface CommunityPost {
  id: string;
  title: string;
  content: string;
  authorId: string;
  authorType: 'admin' | 'community';
  targetLocations: string[];
  postType: 'announcement' | 'event' | 'notice' | 'emergency';
  status: 'draft' | 'published' | 'archived';
  createdAt: Date;
  expiresAt?: Date;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}
