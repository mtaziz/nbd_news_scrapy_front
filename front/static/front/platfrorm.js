import React, {Component} from 'react'
import $ from "jquery"
import {Navbar} from "react-bootstrap";
import {Button} from 'react-bootstrap';
import {ButtonToolbar} from 'react-bootstrap';
import {Row ,Col} from 'react-bootstrap';

class Box1 extends  Component {
    render() {
        return(
            <Row className="show-grid">
                <Col xs={12} md={12}>
                    <Platform />
                </Col>
            </Row>
        )
    }
}

class Platform extends Component {
    constructor(props) {
        super(props);
        this.state = {Platform:["NBD", "QQ", "sina"]};
    }
    render() {
            return (

               <ButtonToolbar>
                    <span className="pull-left">文章平台：</span>
                {
                    this.state.Platform.map (
                        (name,index)  => <Button bsStyle="primary" key={index}> {name} </Button>
                    )
                }
               </ButtonToolbar>
            )

    }
}
export default Box1