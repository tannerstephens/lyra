import React from 'react';
import { Section, Container } from 'bloomer';
import Nav from './base/Nav';
import Pages from './base/Pages';
import '../styles/base.scss';

class Base extends React.Component {
  state = {};

  render() {
    return (
      <div>
        <Nav />
        <Section>
          <Container>
            <Pages />
          </Container>
        </Section>
      </div> 
    );
  }
}
 
export default Base;