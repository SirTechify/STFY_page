import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FaGithub, FaLinkedin, FaEnvelope } from 'react-icons/fa';
import MailingList from './mailingList';

const Container = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  color: white;
  padding: 2rem;
`;

const Header = styled(motion.header)`
  text-align: center;
  margin-bottom: 4rem;
`;

const Title = styled.h1`
  font-size: 4rem;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
`;

const Subtitle = styled.h2`
  font-size: 1.5rem;
  margin: 1rem 0;
  color: #888;
`;

const SocialLinks = styled.div`
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 2rem;
`;

const SocialIcon = styled(motion.a)`
  font-size: 2rem;
  color: white;
  transition: color 0.3s ease;
  &:hover {
    color: #4ecdc4;
  }
`;

function App() {
  return (
    <Container>
      <Header
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <Title>SirTechify</Title>
        <Subtitle>Engineer & Emerging Tech Enthusiast</Subtitle>
        <SocialLinks>
          <SocialIcon
            href="https://github.com/SirTechify"
            target="_blank"
            rel="noopener noreferrer"
            whileHover={{ scale: 1.2 }}
          >
            <FaGithub />
          </SocialIcon>
          <SocialIcon
            href="https://www.linkedin.com/in/sirtechify/"
            target="_blank"
            rel="noopener noreferrer"
            whileHover={{ scale: 1.2 }}
          >
            <FaLinkedin />
          </SocialIcon>
          <SocialIcon
            href="mailto:sirtechify@gmail.com"
            target="_blank"
            rel="noopener noreferrer"
            whileHover={{ scale: 1.2 }}
          >
            <FaEnvelope />
          </SocialIcon>
        </SocialLinks>
      </Header>
      <MailingList />
    </Container>
  );
}

export default App;
