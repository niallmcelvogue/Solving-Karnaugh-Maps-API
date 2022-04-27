import { Navbar, Nav, Container } from 'react-bootstrap';

const Navigation = () => {
    return (
        <>
            <Navbar collapseOnSelect fixed={'top'} expand={'sm'} bg={'dark'} variant={'dark'}>
            <Container>
                <Navbar.Toggle aria-controls={'response-navbar-nav'}/>
                <Navbar.Collapse id={'responsive-navbar-nav'}/>
                <Nav>
                    <h4>K-Map Solver</h4>
                    <Nav.Link href={'/'}>Home</Nav.Link>
                     <Nav.Link href={'/manual'}>Manual</Nav.Link>
                    <Nav.Link href={'/upload'}>Upload</Nav.Link>
                    <Nav.Link href={'/table'}>Table</Nav.Link>
                </Nav>
            </Container>
            </Navbar>
        </>
    )
}

export default Navigation;