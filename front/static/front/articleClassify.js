import React, {Component} from 'react'
import $ from "jquery"
import {Navbar} from "react-bootstrap";
import {Button} from 'react-bootstrap';
import {ButtonToolbar} from 'react-bootstrap';
import {Row, Col, Modal, Grid, Panel, Well, FormGroup, InputGroup, FormControl, ListGroup, ListGroupItem} from 'react-bootstrap';
import Select2 from 'react-select2-wrapper';

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
        this.setInit = this.setInit.bind(this);
    }
    setInit() {
        $.getJSON(" /user/favorite").then( msg => {
            var initName =[];
            var curArticleClassifyId = [];
            var curPlatformId = [];
            var curAllmediaId = [];
            function newArray(json , arrayName) {
                if (json.length  == 0) {
                    return false;
                }
                for (var value of json) {
                    initName.push(value.name);
                    arrayName.push(value.id);
                }
            }
            newArray(msg.user_favorite_crawl_media_sort,curArticleClassifyId);
            newArray(msg.user_favorite_crawl_dir_sort,curPlatformId);
            newArray(msg.user_favorite_crawl_media,curAllmediaId);
            this.setState({
                curArticleClassifyId:curArticleClassifyId,
                curPlatformId:curPlatformId,
                curAllmediaId:curAllmediaId,
                curItem:initName
            })
            console.log(curArticleClassifyId);
        })
    }
    componentDidMount() {
       this.setInit();
    }

    componentWillUnmount() {
        this.serverRequest.abort();
    }
    changeItem(item, elem) {

        var newCurItem = this.state.curItem;
        var newCurPlatform = this.state.curPlatform;
        var newCurArticleClassify = this.state.curArticleClassify;
        var newCurAllmedia = this.state.curAllmedia;
        var newCurPlatformId = this.state.curPlatformId;
        var newCurArticleClassifyId = this.state.curArticleClassifyId;
        var newCurAllmediaId = this.state.curAllmediaId;
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

        // console.log("curAllmediaId=" + this.state.curAllmediaId)
    }

    render() {
        // console.log("TIME = " + this.state.Time)
        return (
            <div>
                <Box changePlatform={this.changeItem} curItem={this.state.curItem}/>
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
// <Box1 changePlatform={this.changeItem} curItem={this.state.curItem}/>

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
        this.state = {articleClassify: [],open:true};
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
                <Panel header= { <h3>网站分类<a href="javascript:void(0)" className="pull-right" onClick = { () => this.setState({ open: !this.state.open })} >{this.state.open? "关闭" :"展开" }</a></h3> } collapsible expanded={this.state.open}>
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
        this.state = {Platform: [],open:false};
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
                <Panel header={<h3>所有网站<a href="javascript:void(0)" className="pull-right" onClick = { () => this.setState({ open: !this.state.open })} >{this.state.open? "关闭" :"展开" }</a></h3>}  collapsible expanded={this.state.open} >
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
        this.sendKeywords =this.sendKeywords.bind(this);
    }

    getArticleList(nextProps) {
        $.getJSON("/get_article", {
            "user_favorite_crawl_media_sort": nextProps.curArticleClassifyId.join(","),
            "user_favorite_crawl_dir_sort": nextProps.curPlatformId.join(","),
            "SendTime": this.props.time,
            "user_favorite_crawl_media": nextProps.curAllmediaId.join(",")
        }).then(msg => {
            console.log(nextProps)
            var post = msg;
            // var newPost = this.state.articleList.slice().concat(post);
            this.setState({articleList: post, Data: nextProps})
        })
    }
    sendKeywords () {
        $.post("/user/update_favorite",{
            "user_favorite_crawl_media_sort" : this.state.Data.curArticleClassifyId.join(","),
            "user_favorite_crawl_dir_sort": this.state.Data.curPlatformId.join(","),
            "user_favorite_crawl_media": this.state.Data.curAllmediaId.join(",")
        }).then( msg => {
            alert(msg)
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
                      curArticleClassify={this.props.curArticleClassify} sendKeywords = {this.sendKeywords}/>
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
                <Button bsStyle="info" onClick = { this.props.sendKeywords }>收藏该组标签</Button>
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
                <Button bsStyle="info" onClick={ () => this.setState({open: !this.state.open})}> { this.state.open ? "隐藏文章主体" : "显示文章主体"} </Button>
                <Button href={this.props.article.article_true_link} target="_blank"
                        style={{marginLeft: 15}}>查看原网页</Button>
                 <Button href={this.props.article.link} target="_blank"
                        style={{marginLeft: 15}}>前往编辑</Button>
                <i><b> 更新时间：{this.props.article.article_published_at} 来源： {this.props.article.media_name} </b></i>
                <div  className="col-xs-12 col-md-12">
                </div>

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