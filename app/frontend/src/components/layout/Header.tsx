/** Global navigation header component */
import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Menu,
  MenuItem,
  Avatar,
  Box,
  useTheme,
  useMediaQuery,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from "@mui/material";
import {
  Home,
  Menu as MenuIcon,
  AccountCircle,
  Settings,
  Logout,
  Brightness4,
  Brightness7,
  School,
  Assessment,
  TrendingUp,
} from "@mui/icons-material";
import { useAuth } from "../../contexts/AuthContext";

export const Header: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [themeMode, setThemeMode] = useState<"light" | "dark">("dark");

  const handleUserMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleUserMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = async () => {
    handleUserMenuClose();
    await logout();
    navigate("/login");
  };

  const handleThemeToggle = () => {
    // TODO: Implement theme toggle with context
    setThemeMode(themeMode === "dark" ? "light" : "dark");
  };

  const isActive = (path: string) => {
    if (path === "/") {
      return location.pathname === "/";
    }
    return location.pathname.startsWith(path);
  };

  // Base navigation items available to all users
  const baseNavItems = [
    { label: "Home", path: "/", icon: <Home /> },
    { label: "Modules", path: "/", icon: <School /> },
    { label: "Progress", path: "/progress", icon: <TrendingUp /> },
    { label: "Assessments", path: "/assessments", icon: <Assessment /> },
  ];

  // Instructor-specific navigation items
  const instructorNavItems = [
    { label: "Instructor Dashboard", path: "/instructor/dashboard", icon: <School /> },
    { label: "Cohorts", path: "/instructor/cohorts", icon: <School /> },
    { label: "Grading", path: "/instructor/grading", icon: <Assessment /> },
  ];

  // Admin-specific navigation items
  const adminNavItems = [
    { label: "Admin Dashboard", path: "/admin/dashboard", icon: <Settings /> },
    { label: "Users", path: "/admin/users", icon: <AccountCircle /> },
    { label: "Settings", path: "/admin/settings", icon: <Settings /> },
  ];

  // Build navigation items based on user role
  const getNavItems = () => {
    const items = [...baseNavItems];
    
    if (user?.role === "instructor" || user?.role === "admin") {
      items.push(...instructorNavItems);
    }
    
    if (user?.role === "admin") {
      items.push(...adminNavItems);
    }
    
    return items;
  };

  const navItems = getNavItems();

  return (
    <>
      <AppBar
        position="sticky"
        sx={{
          background: "rgba(22, 27, 34, 0.9)",
          backdropFilter: "blur(20px)",
          borderBottom: "1px solid rgba(255, 255, 255, 0.1)",
          boxShadow: "0 4px 20px rgba(0, 0, 0, 0.3)",
          width: "100%",
          maxWidth: "100vw",
          overflowX: "hidden",
        }}
      >
        <Toolbar sx={{ justifyContent: "space-between", width: "100%", maxWidth: "100%", overflowX: "hidden", px: { xs: 1, sm: 2 } }}>
          {/* Logo/Brand */}
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              cursor: "pointer",
              gap: 2,
            }}
            onClick={() => navigate("/")}
          >
            <School sx={{ color: "primary.main" }} />
            <Typography
              variant="h6"
              component="div"
              sx={{
                fontWeight: 700,
                color: "white",
                display: { xs: "none", sm: "block" },
              }}
            >
              Crypto Curriculum
            </Typography>
          </Box>

          {/* Desktop Navigation */}
          {!isMobile && (
            <Box
              sx={{
                display: "flex",
                gap: 1,
                flex: 1,
                justifyContent: "center",
                ml: 4,
                flexWrap: "wrap",
                overflowX: "auto",
                maxWidth: "100%",
              }}
            >
              {navItems.map((item) => (
                <Button
                  key={`${item.path}-${item.label}`}
                  startIcon={item.icon}
                  onClick={() => navigate(item.path)}
                  sx={{
                    color: isActive(item.path) ? "primary.main" : "rgba(255, 255, 255, 0.7)",
                    fontWeight: isActive(item.path) ? 600 : 400,
                    whiteSpace: "nowrap",
                    minWidth: "auto",
                    "&:hover": {
                      color: "primary.main",
                      background: "rgba(255, 255, 255, 0.05)",
                    },
                  }}
                >
                  {item.label}
                </Button>
              ))}
            </Box>
          )}

          {/* Right Side Actions */}
          <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
            {/* Theme Toggle */}
            <IconButton
              onClick={handleThemeToggle}
              sx={{
                color: "white",
                "&:hover": {
                  background: "rgba(255, 255, 255, 0.1)",
                },
              }}
            >
              {themeMode === "dark" ? <Brightness7 /> : <Brightness4 />}
            </IconButton>

            {/* Mobile Menu Button */}
            {isMobile && (
              <IconButton
                onClick={() => setMobileMenuOpen(true)}
                sx={{
                  color: "white",
                  "&:hover": {
                    background: "rgba(255, 255, 255, 0.1)",
                  },
                }}
              >
                <MenuIcon />
              </IconButton>
            )}

            {/* User Menu */}
            {!isMobile && (
              <>
                <IconButton
                  onClick={handleUserMenuOpen}
                  sx={{
                    color: "white",
                    "&:hover": {
                      background: "rgba(255, 255, 255, 0.1)",
                    },
                  }}
                >
                  <Avatar
                    sx={{
                      width: 32,
                      height: 32,
                      bgcolor:
                        user?.role === "admin"
                          ? "#f06292"
                          : user?.role === "instructor"
                          ? "#64b5f6"
                          : "primary.main",
                    }}
                  >
                    {user?.full_name?.[0]?.toUpperCase() || user?.email?.[0]?.toUpperCase() || "U"}
                  </Avatar>
                </IconButton>
                <Menu
                  anchorEl={anchorEl}
                  open={Boolean(anchorEl)}
                  onClose={handleUserMenuClose}
                  anchorOrigin={{
                    vertical: "bottom",
                    horizontal: "right",
                  }}
                  transformOrigin={{
                    vertical: "top",
                    horizontal: "right",
                  }}
                  PaperProps={{
                    sx: {
                      background: "rgba(22, 27, 34, 0.95)",
                      backdropFilter: "blur(20px)",
                      border: "1px solid rgba(255, 255, 255, 0.1)",
                      mt: 1,
                    },
                  }}
                >
                  <MenuItem
                    onClick={() => {
                      handleUserMenuClose();
                      navigate("/profile");
                    }}
                    sx={{ color: "white" }}
                  >
                    <AccountCircle sx={{ mr: 2 }} />
                    Profile
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      handleUserMenuClose();
                      navigate("/settings");
                    }}
                    sx={{ color: "white" }}
                  >
                    <Settings sx={{ mr: 2 }} />
                    Settings
                  </MenuItem>
                  <MenuItem onClick={handleLogout} sx={{ color: "white" }}>
                    <Logout sx={{ mr: 2 }} />
                    Sign Out
                  </MenuItem>
                </Menu>
              </>
            )}
          </Box>
        </Toolbar>
      </AppBar>

      {/* Mobile Drawer */}
      <Drawer
        anchor="right"
        open={mobileMenuOpen}
        onClose={() => setMobileMenuOpen(false)}
        PaperProps={{
          sx: {
            background: "rgba(22, 27, 34, 0.95)",
            backdropFilter: "blur(20px)",
            width: 280,
          },
        }}
      >
        <Box sx={{ p: 2 }}>
          <Box sx={{ display: "flex", alignItems: "center", gap: 2, mb: 3, pb: 2, borderBottom: "1px solid rgba(255, 255, 255, 0.1)" }}>
            <Avatar
              sx={{
                bgcolor:
                  user?.role === "admin"
                    ? "#f06292"
                    : user?.role === "instructor"
                    ? "#64b5f6"
                    : "primary.main",
              }}
            >
              {user?.full_name?.[0]?.toUpperCase() || user?.email?.[0]?.toUpperCase() || "U"}
            </Avatar>
            <Box>
              <Typography variant="body1" sx={{ color: "white", fontWeight: 600 }}>
                {user?.full_name || user?.username || "User"}
              </Typography>
              <Typography variant="body2" sx={{ color: "rgba(255, 255, 255, 0.7)" }}>
                {user?.email}
              </Typography>
              {user?.role && (
                <Typography
                  variant="caption"
                  sx={{
                    color: user.role === "admin" ? "#f06292" : user.role === "instructor" ? "#64b5f6" : "rgba(255, 255, 255, 0.5)",
                    textTransform: "capitalize",
                    fontWeight: 600,
                    mt: 0.5,
                  }}
                >
                  {user.role}
                </Typography>
              )}
            </Box>
          </Box>

          <List>
            {navItems.map((item) => (
              <ListItem key={item.path} disablePadding>
                <ListItemButton
                  onClick={() => {
                    navigate(item.path);
                    setMobileMenuOpen(false);
                  }}
                  selected={isActive(item.path)}
                  sx={{
                    color: isActive(item.path) ? "primary.main" : "rgba(255, 255, 255, 0.7)",
                    "&.Mui-selected": {
                      background: "rgba(255, 255, 255, 0.1)",
                    },
                    "&:hover": {
                      background: "rgba(255, 255, 255, 0.05)",
                    },
                  }}
                >
                  <ListItemIcon sx={{ color: "inherit" }}>{item.icon}</ListItemIcon>
                  <ListItemText primary={item.label} />
                </ListItemButton>
              </ListItem>
            ))}
            <ListItem disablePadding>
              <ListItemButton
                onClick={() => {
                  navigate("/profile");
                  setMobileMenuOpen(false);
                }}
                sx={{
                  color: "rgba(255, 255, 255, 0.7)",
                  "&:hover": {
                    background: "rgba(255, 255, 255, 0.05)",
                  },
                }}
              >
                <ListItemIcon sx={{ color: "inherit" }}>
                  <AccountCircle />
                </ListItemIcon>
                <ListItemText primary="Profile" />
              </ListItemButton>
            </ListItem>
            <ListItem disablePadding>
              <ListItemButton
                onClick={() => {
                  navigate("/settings");
                  setMobileMenuOpen(false);
                }}
                sx={{
                  color: "rgba(255, 255, 255, 0.7)",
                  "&:hover": {
                    background: "rgba(255, 255, 255, 0.05)",
                  },
                }}
              >
                <ListItemIcon sx={{ color: "inherit" }}>
                  <Settings />
                </ListItemIcon>
                <ListItemText primary="Settings" />
              </ListItemButton>
            </ListItem>
            <ListItem disablePadding>
              <ListItemButton
                onClick={handleLogout}
                sx={{
                  color: "rgba(255, 255, 255, 0.7)",
                  "&:hover": {
                    background: "rgba(255, 255, 255, 0.05)",
                  },
                }}
              >
                <ListItemIcon sx={{ color: "inherit" }}>
                  <Logout />
                </ListItemIcon>
                <ListItemText primary="Sign Out" />
              </ListItemButton>
            </ListItem>
          </List>
        </Box>
      </Drawer>
    </>
  );
};

