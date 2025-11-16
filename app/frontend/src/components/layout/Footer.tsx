/** Footer component with copyright, support links, and social media */
import React from 'react';
import { Box, Container, Typography, Link, Stack, Divider } from '@mui/material';
import {
  Email,
  Help,
  PrivacyTip,
  Description,
  GitHub,
  Twitter,
  LinkedIn,
  YouTube,
} from '@mui/icons-material';
import { useThemeMode } from '../../contexts/ThemeContext';

export const Footer: React.FC = () => {
  const { mode } = useThemeMode();

  const currentYear = new Date().getFullYear();

  const footerLinks = {
    support: [
      { label: 'Help Center', href: '/help', icon: <Help fontSize="small" /> },
      { label: 'Contact Us', href: '/contact', icon: <Email fontSize="small" /> },
      { label: 'Privacy Policy', href: '/privacy', icon: <PrivacyTip fontSize="small" /> },
      { label: 'Terms of Service', href: '/terms', icon: <Description fontSize="small" /> },
    ],
    social: [
      { label: 'GitHub', href: 'https://github.com', icon: <GitHub /> },
      { label: 'Twitter', href: 'https://twitter.com', icon: <Twitter /> },
      { label: 'LinkedIn', href: 'https://linkedin.com', icon: <LinkedIn /> },
      { label: 'YouTube', href: 'https://youtube.com', icon: <YouTube /> },
    ],
  };

  return (
    <Box
      component="footer"
      sx={{
        backgroundColor: mode === 'light' ? '#ffffff' : '#0a0e27',
        borderTop:
          mode === 'light'
            ? '1px solid rgba(0, 0, 0, 0.1)'
            : '1px solid rgba(255, 255, 255, 0.1)',
        mt: 'auto',
        py: 4,
      }}
    >
      <Container maxWidth="lg">
        <Stack spacing={3}>
          {/* Main Footer Content */}
          <Box
            sx={{
              display: 'flex',
              flexDirection: { xs: 'column', md: 'row' },
              justifyContent: 'space-between',
              alignItems: { xs: 'flex-start', md: 'center' },
              gap: 3,
            }}
          >
            {/* Left: Support Links */}
            <Stack
              direction={{ xs: 'column', sm: 'row' }}
              spacing={{ xs: 2, sm: 4 }}
              sx={{ flexWrap: 'wrap' }}
            >
              {footerLinks.support.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 0.5,
                    color:
                      mode === 'light'
                        ? 'rgba(0, 0, 0, 0.7)'
                        : 'rgba(255, 255, 255, 0.7)',
                    textDecoration: 'none',
                    fontSize: '0.875rem',
                    '&:hover': {
                      color: mode === 'light' ? '#1976d2' : '#4dabf7',
                    },
                  }}
                >
                  {link.icon}
                  {link.label}
                </Link>
              ))}
            </Stack>

            {/* Right: Social Links */}
            <Stack direction="row" spacing={2}>
              {footerLinks.social.map((social) => (
                <Link
                  key={social.label}
                  href={social.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color:
                      mode === 'light'
                        ? 'rgba(0, 0, 0, 0.7)'
                        : 'rgba(255, 255, 255, 0.7)',
                    '&:hover': {
                      color: mode === 'light' ? '#1976d2' : '#4dabf7',
                    },
                    transition: 'color 0.2s',
                  }}
                  aria-label={social.label}
                >
                  {social.icon}
                </Link>
              ))}
            </Stack>
          </Box>

          <Divider
            sx={{
              borderColor:
                mode === 'light'
                  ? 'rgba(0, 0, 0, 0.1)'
                  : 'rgba(255, 255, 255, 0.1)',
            }}
          />

          {/* Copyright */}
          <Box
            sx={{
              display: 'flex',
              flexDirection: { xs: 'column', sm: 'row' },
              justifyContent: 'space-between',
              alignItems: 'center',
              gap: 1,
            }}
          >
            <Typography
              variant="body2"
              sx={{
                color:
                  mode === 'light'
                    ? 'rgba(0, 0, 0, 0.6)'
                    : 'rgba(255, 255, 255, 0.6)',
                textAlign: { xs: 'center', sm: 'left' },
              }}
            >
              © {currentYear} Crypto Curriculum Platform. All rights reserved.
            </Typography>
            <Typography
              variant="body2"
              sx={{
                color:
                  mode === 'light'
                    ? 'rgba(0, 0, 0, 0.6)'
                    : 'rgba(255, 255, 255, 0.6)',
                textAlign: { xs: 'center', sm: 'right' },
              }}
            >
              Universal Tech Movement
            </Typography>
          </Box>
        </Stack>
      </Container>
    </Box>
  );
};

