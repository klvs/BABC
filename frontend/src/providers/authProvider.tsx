// authProvider.tsx
import React, { useState, useEffect, ReactNode } from "react";
import { useQuery } from "react-query";
import AuthContext, { AuthContextType } from "../contexts/authContext";

type AuthProviderProps = {
  children: ReactNode;
};

const fetchUser = async () => {
  const response = await fetch(`/api/user/`);
  if (response.ok) {
    return response.json();
  }

  if (response.status === 403) {
    return null;
  }

  throw new Error(response.status.toString());
};

const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  const { data } = useQuery("user", fetchUser, {
    staleTime: 2 * 60 * 60 * 1000, // 2 hours in milliseconds
    retry: false,
    onError: (error: Error) => {
      console.log(error.message);
    },
  });

  useEffect(() => {
    if (data) {
      setIsAuthenticated(true);
      setUser(data);
    }
  }, [data]);

  const login = async () => {
    // Redirect the user to the Discord authentication page
    window.location.href = `/login/discord/`;
  };

  const logout = async () => {
    // Make a POST request to the logout endpoint
    const response = await fetch(`/api/logout/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        // Include your authentication headers, e.g., Bearer token
      },
    });

    if (response.ok) {
      // If the response is OK, the user was logged out successfully
      setIsAuthenticated(false);
      setUser(null);
    } else {
      // Handle any errors
    }
  };

  const authContextValue: AuthContextType = {
    isAuthenticated,
    login,
    logout,
    user,
  };

  return (
    <AuthContext.Provider value={authContextValue}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
