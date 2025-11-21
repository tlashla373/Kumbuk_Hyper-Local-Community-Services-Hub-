import React from 'react';
import { View, StyleSheet } from 'react-native';
import { AgentChat } from '../components/AgentChat';

export const ChatScreen = () => {
  // TODO: Get actual user ID from authentication
  const userId = 'consumer_123';

  return (
    <View style={styles.container}>
      <AgentChat userId={userId} apiUrl="http://localhost:8000" />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});

export default ChatScreen;
