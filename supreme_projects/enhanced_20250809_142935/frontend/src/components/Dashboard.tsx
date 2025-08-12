```typescript
// src/components/Dashboard/Dashboard.tsx

import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  fetchUserData,
  uploadFiles,
  sendMessage,
  fetchMessages,
  processPayment,
  sendNotification,
  fetchAnalyticsData,
  createUser,
  updateUser,
  deleteUser,
} from '../../api'; // Replace with your actual API calls
import { User, Message, AnalyticsData, PaymentDetails } from '../../types'; // Replace with your actual types
import FileUpload from './FileUpload'; // Example sub-component
import Chat from './Chat'; // Example sub-component
import Analytics from './Analytics'; // Example sub-component
import UserManagement from './UserManagement'; // Example sub-component
import { useToast } from '../../context/ToastContext'; // Example toast context
import { validateProps } from './Dashboard.validation'; // Prop validation function


interface DashboardProps {
  userId: string;
  isAdmin: boolean;
}

const Dashboard: React.FC<DashboardProps> = ({ userId, isAdmin }) => {
  const { addToast } = useToast();
  const { queryClient } = useQueryClient();
  const params = useParams();
  const [isLoading, setIsLoading] = useState(true);
  const [userData, setUserData] = useState<User | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [paymentProcessing, setPaymentProcessing] = useState(false);
  const [paymentError, setPaymentError] = useState<string | null>(null);


  const { data: fetchedUserData, isLoading: isUserDataLoading, error: userDataError } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUserData(userId),
    enabled: !!userId,
    onSuccess: (data) => {
      setUserData(data);
    },
  });

  const { data: fetchedAnalyticsData, isLoading: isAnalyticsLoading, error: analyticsError } = useQuery({
    queryKey: ['analytics'],
    queryFn: fetchAnalyticsData,
    enabled: isAdmin,
    onSuccess: (data) => {
      setAnalyticsData(data);
    },
  });

  const { data: fetchedMessages, isLoading: isMessagesLoading, error: messagesError } = useQuery({
    queryKey: ['messages'],
    queryFn: fetchMessages,
    enabled: true,
    onSuccess: (data) => {
      setMessages(data);
    },
  });


  const uploadMutation = useMutation(uploadFiles, {
    onSuccess: () => {
      addToast({ type: 'success', message: 'Files uploaded successfully!' });
      queryClient.invalidateQueries(['user', userId]); //Invalidate cache after upload
    },
    onError: (error) => {
      addToast({ type: 'error', message: `File upload failed: ${error.message}` });
    },
  });

  const sendMessageMutation = useMutation(sendMessage, {
    onSuccess: () => {
      setNewMessage('');
      queryClient.invalidateQueries(['messages']);
    },
    onError: (error) => {
      addToast({ type: 'error', message: `Failed to send message: ${error.message}` });
    },
  });

  const processPaymentMutation = useMutation(processPayment, {
    onSuccess: () => {
      setPaymentProcessing(false);
      addToast({ type: 'success', message: 'Payment processed successfully!' });
    },
    onError: (error) => {
      setPaymentProcessing(false);
      setPaymentError(error.message);
      addToast({ type: 'error', message: `Payment failed: ${error.message}` });
    },
  });

  const handleSendMessage = useCallback(() => {
    if (newMessage.trim() !== '') {
      sendMessageMutation.mutate({ message: newMessage });
    }
  }, [newMessage, sendMessageMutation]);

  const handlePayment = useCallback(async (paymentDetails: PaymentDetails) => {
    setPaymentProcessing(true);
    setPaymentError(null);
    try {
      await processPaymentMutation.mutateAsync(paymentDetails);
    } catch (error) {
      //Error already handled in mutation
    }
  }, [processPaymentMutation]);


  useEffect(() => {
    setIsLoading(false);
  }, [isUserDataLoading, isAnalyticsLoading, isMessagesLoading]);


  //Error Handling
  if (userDataError || analyticsError || messagesError) {
    return <div className="p-4 text-red-500">Error loading data. Please try again later.</div>;
  }

  //Loading State
  if (isLoading) {
    return <div className="p-4">Loading...</div>;
  }

  //Prop Validation
  validateProps({userId, isAdmin});


  return (
    <div className="flex flex-col md:flex-row h-screen">
      {/* Left Side: User Info & File Upload */}
      <div className="w-full md:w-1/3 p-4">
        {userData && (
          <div>
            <h2 className="text-2xl font-bold mb-4">User Profile</h2>
            <p>ID: {userData.id}</p>
            <p>Name: {userData.name}</p>
            {/* ... other user details ... */}
            <FileUpload onUpload={uploadMutation.mutate} />
          </div>
        )}
        {isAdmin && (
          <UserManagement
            createUser={createUser}
            updateUser={updateUser}
            deleteUser={deleteUser}
            queryClient={queryClient}
            addToast={addToast}
          />
        )}
      </div>

      {/* Right Side: Chat & Analytics */}
      <div className="w-full md:w-2/3 p-4">
        <div className="mb-4">
          <Chat messages={messages} onSendMessage={handleSendMessage} newMessage={newMessage} setNewMessage={setNewMessage} />
        </div>
        {isAdmin && analyticsData && (
          <Analytics data={analyticsData} />
        )}
        {isAdmin && (
          <div>
            <button
              onClick={() => handlePayment({ amount: 100, currency: 'USD' })}
              disabled={paymentProcessing}
              className