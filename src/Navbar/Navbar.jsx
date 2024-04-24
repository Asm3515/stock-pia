import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom'; // Import NavLink from react-router-dom
import './Navbar.css';
import logo from '../Assets/logo.webp';

function Navbar() {
  const [navActive, setNavActive] = useState(false);

  const toggleNav = () => {
    setNavActive(!navActive);
  };

  const closeMenu = () => {
    setNavActive(false);
  };

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth <= 500) {
        closeMenu();
      }
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  useEffect(() => {
    if (window.innerWidth <= 1200) {
      closeMenu();
    }
  }, []);

  return (
    <nav className={`navbar ${navActive ? 'active' : ''}`}>
      <div>
        <img className="navbar_logo" src={logo} alt="Logoipsum" />
      </div>
      <a className={`nav__hamburger ${navActive ? 'active' : ''}`} onClick={toggleNav}>
        <span className="nav__hamburger__line"></span>
        <span className="nav__hamburger__line"></span>
        <span className="nav__hamburger__line"></span>
      </a>
      <div className={`navbar--items ${navActive ? 'active' : ''}`}>
        <ul>
          <li>
            <NavLink // Change Link to NavLink
              onClick={closeMenu}
              activeClassName="navbar--active-content" // Use activeClassName for active class
              to="/" // Specify the path to navigate to
              className="navbar--content"
              exact // Add exact to match exact path
            >
              HOME
            </NavLink>
          </li>
          <li>
            <NavLink // Change Link to NavLink
              onClick={closeMenu}
              activeClassName="navbar--active-content" // Use activeClassName for active class
              to="/sp500" // Specify the path to navigate to
              className="navbar--content"
            >
              SP500
            </NavLink>
          </li>
          <li>
            <NavLink // Change Link to NavLink
              onClick={closeMenu}
              activeClassName="navbar--active-content" // Use activeClassName for active class
              to="/nasdaq" // Specify the path to navigate to
              className="navbar--content"
            >
              NASDAQ
            </NavLink>
          </li>
          <li>
            <NavLink // Change Link to NavLink
              onClick={closeMenu}
              activeClassName="navbar--active-content" // Use activeClassName for active class
              to="/history" // Specify the path to navigate to
              className="navbar--content"
            >
              HISTORY
            </NavLink>
          </li>
        </ul>
      </div>
      <NavLink // Change Link to NavLink
        onClick={closeMenu}
        activeClassName="navbar--active-content" // Use activeClassName for active class
        to="/contact" // Specify the path to navigate to
        className="btn btn-outline-primary"
      >
        Powered by - React, Flask and Yfinance
      </NavLink>
    </nav>
  );
}

export default Navbar;
