import React from 'react';
import {
  NavbarEnd,
  NavbarItem,
  NavbarDropdown,
  NavbarLink,
  NavbarDivider
} from 'bloomer';

const LoggedInItems = (props) => {
  return (
    <NavbarEnd>
      <NavbarItem hasDropdown isHoverable>
        <NavbarLink>{props.user.name}</NavbarLink>
        <NavbarDropdown>
          <NavbarItem>Manage Groups</NavbarItem>
          <NavbarDivider />
          <NavbarItem>Logout</NavbarItem>
        </NavbarDropdown>       
      </NavbarItem>
    </NavbarEnd>
  );
}
 
export default LoggedInItems;