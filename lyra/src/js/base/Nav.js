import React from 'react';
import {
  Container,
  Image,
  Navbar,
  NavbarBrand,
  NavbarBurger,
  NavbarMenu,
  NavbarItem,
  NavbarLink,
} from 'bloomer';
import logo from '../../images/logo.png';
import LoggedInItems from './nav/LoggedInItems';

class Nav extends React.Component {
  state = {
    active: false,
  };

  toggleNav = () => {
    this.setState({
      active: !this.state.active,
    });
  }

  render() {
    const userObject = {
      name: 'Tanner Stephens'
    };

    return (
      <Navbar>
        <Container>
          <NavbarBrand>
            <NavbarItem href="/">
              <Image src={logo} />
            </NavbarItem>
            <NavbarBurger
              isActive={this.state.active}
              onClick={this.toggleNav}
            />
          </NavbarBrand>
          <NavbarMenu isActive={this.state.active}>
            <LoggedInItems user={userObject} />
          </NavbarMenu>
        </Container>
      </Navbar>
    );
  }
}
 
export default Nav;