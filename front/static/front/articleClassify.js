import React, {Component} from 'react'
import $ from "jquery"
import {Navbar} from "react-bootstrap";
import {Button} from 'react-bootstrap';
import {ButtonToolbar} from 'react-bootstrap';
import {Row, Col, Modal, Grid, Panel, Well, FormGroup, InputGroup, FormControl, ListGroup, ListGroupItem} from 'react-bootstrap';

class Parents extends Component {
    constructor(props) {
        super(props);
        this.state = {
            curItem: [],
            curPlatform: [],
            curPlatformId: [],
            curArticleClassify: [],
            curArticleClassifyId: [],
            curAllmedia: [],
            curAllmediaId: [],
            Time: ""
        };
        this.changeItem = this.changeItem.bind(this);

    }

    changeItem(item, elem) {

        var newCurItem = this.state.curItem.slice();
        var newCurPlatform = this.state.curPlatform.slice();
        var newCurArticleClassify = this.state.curArticleClassify.slice();
        var newCurAllmedia = this.state.curAllmedia.slice();
        var newCurPlatformId = this.state.curPlatformId.slice();
        var newCurArticleClassifyId = this.state.curArticleClassifyId.slice();
        var newCurAllmediaId = this.state.curAllmediaId.slice();
        if (elem == 'Platform') {
            newCurPlatform.indexOf(item[1]) == -1 ? newCurPlatform.push(item[1]) : newCurPlatform.splice(newCurPlatform.indexOf(item[1]), 1);
            newCurPlatformId.indexOf(item[0]) == -1 ? newCurPlatformId.push(item[0]) : newCurPlatformId.splice(newCurPlatformId.indexOf(item[0]), 1);

        } else if (elem == 'ArticleClassify') {
            newCurArticleClassify.indexOf(item[1]) == -1 ? newCurArticleClassify.push(item[1]) : newCurArticleClassify.splice(newCurArticleClassify.indexOf(item[1]), 1);
            newCurArticleClassifyId.indexOf(item[0]) == -1 ? newCurArticleClassifyId.push(item[0]) : newCurArticleClassifyId.splice(newCurArticleClassifyId.indexOf(item[0]), 1);
        } else if (elem == "Allmedia") {
            newCurAllmedia.indexOf(item[1]) == -1 ? newCurAllmedia.push(item[1]) : newCurAllmedia.splice(newCurAllmedia.indexOf(item[1]), 1);
            newCurAllmediaId.indexOf(item[0]) == -1 ? newCurAllmediaId.push(item[0]) : newCurAllmediaId.splice(newCurAllmediaId.indexOf(item[0]), 1);
        }
        newCurItem.indexOf(item[1]) == -1 ? newCurItem.push(item[1]) : newCurItem.splice(newCurItem.indexOf(item[1]), 1);
        var beforeSendTime = new Date().getTime();
        this.setState({
            curItem: newCurItem,
            curPlatform: newCurPlatform,
            curArticleClassify: newCurArticleClassify,
            curAllmedia: newCurAllmedia,
            curPlatformId: newCurPlatformId,
            curArticleClassifyId: newCurArticleClassifyId,
            curAllmediaId: newCurAllmediaId,
            Time: beforeSendTime
        })

        console.log("curAllmediaId=" + this.state.curAllmediaId)
    }

    render() {
        console.log("TIME = " + this.state.Time)
        return (
            <div>
                <Box changePlatform={this.changeItem} curItem={this.state.curItem}/>
                /*<Box1 changePlatform={this.changeItem} curItem={this.state.curItem}/>*/
                <Box2 changePlatform={this.changeItem} curItem={this.state.curItem}/>
                <TestWrapper curItem={this.state.curItem} curPlatformId={this.state.curPlatformId}
                             curArticleClassifyId={this.state.curArticleClassifyId}
                             curAllmediaId={this.state.curAllmediaId}
                             time={this.state.Time}
                />
            </div>
        )
    }
}

class Box extends Component {
    constructor(props) {
        super(props);
        this.changePlatformA = this.changePlatformA.bind(this);
    }

    changePlatformA(item, elem) {
        this.props.changePlatform(item, elem)
    }

    render() {
        return (
            <Row className="show-grid">
                <Col xs={12} md={12}>
                    <ArticleClassify changePlatformL={this.changePlatformA} heightLinghtT={this.props.curItem}/>
                </Col>
            </Row>
        )
    }
}

class ArticleClassify extends Component {
    constructor(props) {
        super(props);
        this.state = {articleClassify: []};
    }

    handClick(item, elem = 'ArticleClassify') {
        this.props.changePlatformL(item, elem)
    }

    componentDidMount() {
        $.get("/get_media_sorts").then(msg => {
            const posts = msg;
            this.setState({articleClassify: posts.message})
        })
    }

    componentWillUnmount() {
        this.serverRequest.abort();
    }

    render() {
        return (
            <div>
                <Panel header= { "网站分类" }>
                    {
                        (function () {
                            return this.state.articleClassify.map(
                                (name, index) => this.props.heightLinghtT.slice().indexOf(name.crawl_media_sort_name) == -1 ?
                                    <Button bsStyle="primary" key={name.id}
                                            onClick={this.handClick.bind(this, [name.id, name.crawl_media_sort_name], 'ArticleClassify')}> {name.crawl_media_sort_name} </Button> :
                                    <Button bsStyle="warning" key={name.id}
                                            onClick={this.handClick.bind(this, [name.id, name.crawl_media_sort_name], 'ArticleClassify')}> {name.crawl_media_sort_name} </Button>
                            )
                        }.bind(this))()
                    }
                </Panel>
            </div>
        )

    }
}
class Box1 extends Component {
    constructor(props) {
        super(props);
        this.changePlatformA = this.changePlatformA.bind(this);
    }

    changePlatformA(item, elem = 'Platform') {
        this.props.changePlatform(item, elem)
    }

    render() {
        return (

            <Row className="show-grid">
                <Col xs={12} md={12}>
                    <Platform changePlatformL={this.changePlatformA} heightLinghtT={this.props.curItem}/>
                </Col>
            </Row>

        )
    }
}

class Platform extends Component {
    constructor(props) {
        super(props);
        this.state = {Platform: []};
    }

    handClick(item, elem = 'Platform') {

        this.props.changePlatformL(item, elem)
    }

    componentDidMount() {
        $.get("/get_dir_sorts").then(msg => {
            const posts1 = msg;
            this.setState({Platform: posts1.message})
        })
    }

    componentWillUnmount() {
        this.serverRequest.abort();
    }

    render() {
        console.log("b=" + this.props.heightLinghtT)
        return (
            <div>
                <Panel header="栏目分类">
                    {
                        (function () {
                            return this.state.Platform.map(
                                (name, index) => this.props.heightLinghtT.slice().indexOf(name.crawl_dir_sort_name) == -1 ?
                                    <Button bsStyle="primary" key={name.id}
                                            onClick={this.handClick.bind(this, [name.id, name.crawl_dir_sort_name], 'Platform')}> {name.crawl_dir_sort_name} </Button> :
                                    <Button bsStyle="warning" key={name.id}
                                            onClick={this.handClick.bind(this, [name.id, name.crawl_dir_sort_name], 'Platform')}> {name.crawl_dir_sort_name} </Button>
                            )
                        }.bind(this))()

                    }
                </Panel>
            </div>
        )

    }
}
class Box2 extends Component {
    constructor(props) {
        super(props);
        this.changePlatformA = this.changePlatformA.bind(this);
    }

    changePlatformA(item, elem = 'Platform') {
        this.props.changePlatform(item, elem)
    }

    render() {
        return (

            <Row className="show-grid">
                <Col xs={12} md={12}>
                    <Allmedia changePlatformL={this.changePlatformA} heightLinghtT={this.props.curItem}/>
                </Col>
            </Row>

        )
    }
}

class Allmedia extends Component {
    constructor(props) {
        super(props);
        this.state = {Platform: []};
    }

    handClick(item, elem = 'Allmedia') {

        this.props.changePlatformL(item, elem)
    }

    componentDidMount() {
        $.get("/get_medias").then(msg => {
            const posts1 = msg;
            this.setState({Platform: posts1.message})
        })
    }

    componentWillUnmount() {
        this.serverRequest.abort();
    }

    render() {
        console.log("b=" + this.props.heightLinghtT)
        return (
            <div>
                <Panel header="所有网站">
                    {
                        (function () {
                            return this.state.Platform.map(
                                (name, index) => this.props.heightLinghtT.slice().indexOf(name.crawl_media_name) == -1 ?
                                    <Button bsStyle="primary" key={name.id}
                                            onClick={this.handClick.bind(this, [name.id, name.crawl_media_name], 'Allmedia')}> {name.crawl_media_name} </Button> :
                                    <Button bsStyle="warning" key={name.id}
                                            onClick={this.handClick.bind(this, [name.id, name.crawl_media_name], 'Allmedia')}> {name.crawl_media_name} </Button>
                            )
                        }.bind(this))()

                    }
                </Panel>
            </div>
        )

    }
}

class TestWrapper extends Component {
    constructor(props) {
        super(props);
        this.state = {articleList: [], clear: false, Data: {}};
        // this.testChange = this.testChange.bind(this);
        // this.getArticleList = this.getArticleList.bind(this);
    }

    getArticleList(nextProps) {
        $.getJSON("/get_article", {
            "newCurArticleClassifyl": nextProps.curArticleClassifyId.join(","),
            "Platforml": nextProps.curPlatformId.join(","),
            "SendTime": this.props.time,
            "Allmedia": nextProps.curAllmediaId.join(",")
        }).then(msg => {
            var post = msg;
            // var newPost = this.state.articleList.slice().concat(post);
            this.setState({articleList: post, Data: nextProps})
        })
    }

    componentWillReceiveProps(nextProps) {
        this.getArticleList(nextProps);
        this.setState({
            clear: true,

        })
        var that = this;
        var repeat = setInterval(function () {
            that.getArticleList(that.state.Data);
        }, 10000)
        if (this.state.clear) {
            clearInterval(repeat);
        }
    }

    componentWillUnmount() {
        this.serverRequest.abort();
    }

    render() {
        return (
            <div>
                <List curItem={this.props.curItem} curPlatform={this.props.curPlatform}
                      curArticleClassify={this.props.curArticleClassify}/>
                {
                    this.state.articleList.map(
                        (name, index) => <Modle article={name} key={index}/>
                    )
                }
            </div>
        )
    }
}
class List extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <ButtonToolbar>
                <span className="pull-left">已选择的标签：</span>
                {
                    this.props.curItem.map(
                        (name, index) => <Button bsStyle="primary" key={index}> {name} </Button>
                    )
                }
            </ButtonToolbar>
        )
    }
}
class Modle extends Component {
    constructor(props) {
        super(props);
        this.state = {
            open: false
        };
    }


    render() {
        return (
            <Well className="col-xs-12 col-md-12 articleList" key={this.props.article.pk} onClick={this.showModal}>
                <h3 >{this.props.article.article_title}</h3>
                <p>{this.props.article.article_desc}</p>
                <Panel collapsible expanded={this.state.open}>
                    <div dangerouslySetInnerHTML={{__html: this.props.article.article_content}}></div>
                    <p> {this.props.article.article_origin}</p>
                </Panel>
                <Button bsStyle="info" onClick={ () => this.setState({open: !this.state.open})}> 显示文章主体 </Button>
                <Button href={this.props.article.article_true_link} target="_blank"
                        style={{marginLeft: 15}}>查看原网页</Button>
                <i><b> 更新时间：{this.props.article.article_published_at} 来源： {this.props.article.media_name} </b></i>
            </Well>
        )
    }
}
//search
class Search extends Component {
    constructor(props) {
        super(props);
        this.state = {
            searchList:[],
            open:false,
            value:"",
        }
        this.searcheKeyword = this.searcheKeyword.bind(this);
    }
    searcheKeyword(e) {
        const word = e.target.value;
        this.setState({value:word},()=>{console.log(this.state.value)})
        console.log(this.props.tags)
    }

    render() {
        return (
            <Row>
                <Col xs={5} md={3} className = "pull-right">
                    <FormGroup style={{marginBottom:0,position:"relative"}}>
                        <InputGroup>
                            <FormControl type="text" value={this.state.value}  onChange = {this.searcheKeyword} />
                            <InputGroup.Button>
                                <Button>search</Button>
                            </InputGroup.Button>
                            <ListGroup className="seachList">
                                <ListGroupItem>共有个{this.state.searchList.length}关键词</ListGroupItem>
                            </ListGroup>
                        </InputGroup>
                    </FormGroup>
                </Col>
            </Row>
        )
    }
}
export default Parents