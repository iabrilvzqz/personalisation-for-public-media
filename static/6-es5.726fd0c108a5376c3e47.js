function _classCallCheck(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function _defineProperties(e,t){for(var i=0;i<t.length;i++){var r=t[i];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function _createClass(e,t,i){return t&&_defineProperties(e.prototype,t),i&&_defineProperties(e,i),e}(window.webpackJsonp=window.webpackJsonp||[]).push([[6],{cnSs:function(e,t,i){"use strict";i.r(t),i.d(t,"AuthModule",(function(){return y}));var r=i("ofXK"),n=i("3Pt+"),o=i("1kSV"),s=i("4zvT"),a=i("tyNb"),c=i("fXoL"),l=i("7dP1");function u(e,t){if(1&e&&(c.Pb(0,"ngb-alert",33),c.Cc(1),c.Ob()),2&e){var i=c.cc();c.hc("dismissible",!1),c.xb(1),c.Dc(i.error)}}function b(e,t){if(1&e&&(c.Pb(0,"option"),c.Cc(1),c.Ob()),2&e){var i=t.$implicit;c.xb(1),c.Dc(i.email)}}function d(e,t){1&e&&(c.Pb(0,"div"),c.Cc(1,"Password is required"),c.Ob())}function f(e,t){if(1&e&&(c.Pb(0,"div",34),c.Ac(1,d,2,0,"div",35),c.Ob()),2&e){var i=c.cc();c.xb(1),c.hc("ngIf",i.f.password.errors.required)}}var m,p,h,g=function(e){return{"is-invalid":e}},v=[{path:"login",component:(m=function(){function e(t,i,r,n){_classCallCheck(this,e),this.formBuilder=t,this.route=i,this.router=r,this.authenticationService=n,this.submitted=!1,this.error="",this.year=(new Date).getFullYear(),this.users=[{id:2,email:"albert@students.uu.nl",picture:"avatar-1.jpg",type:"Content Devourer"},{id:3,email:"ilse@students.uu.nl",picture:"avatar-2.jpg",type:"Series Streamer"},{id:4,email:"kevine@students.uu.nl",picture:"avatar-3.jpg",type:"Movie Buff"},{id:7,email:"enrique@students.uu.nl",picture:"avatar-4.jpg",type:"Documentary Lover"}]}return _createClass(e,[{key:"ngOnInit",value:function(){this.loginForm=this.formBuilder.group({email:["albert@students.uu.nl",[n.m.required,n.m.email]],password:["123456",[n.m.required]]}),this.selectUser(this.users[0].email),this.returnUrl=this.route.snapshot.queryParams.returnUrl||"/"}},{key:"ngAfterViewInit",value:function(){}},{key:"onSubmit",value:function(){this.submitted=!0,this.loginForm.invalid||(this.authenticationService.login(this.selectedUser),this.router.navigate(["/dashboard"]))}},{key:"getUserInformation",value:function(e){return this.users.filter((function(t){return t.email===e}))[0]}},{key:"selectUser",value:function(e){this.selectedUser=this.getUserInformation(e)}},{key:"f",get:function(){return this.loginForm.controls}}]),e}(),m.\u0275fac=function(e){return new(e||m)(c.Kb(n.b),c.Kb(a.a),c.Kb(a.c),c.Kb(l.a))},m.\u0275cmp=c.Eb({type:m,selectors:[["app-login"]],decls:42,vars:7,consts:[[1,"account-pages","mt-5","mb-5"],[1,"container"],[1,"row","justify-content-center"],[1,"col-md-8","col-lg-6","col-xl-5"],[1,"card","overflow-hidden"],[1,"bg-soft-primary"],[1,"row"],[1,"col-7"],[1,"text-primary","p-4"],[1,"text-primary"],[1,"col-5","align-self-end"],["src","assets/images/profile-img.png","alt","",1,"img-fluid"],[1,"card-body","pt-0"],["href","/"],[1,"avatar-md","profile-user-wid","mb-4"],[1,"avatar-title","rounded-circle","bg-dark"],["src","assets/images/logo-light-sm.svg","alt","","height","34",1,"rounded-circle"],[1,"p-2"],[1,"form-horizontal",3,"formGroup","ngSubmit"],["type","danger",3,"dismissible",4,"ngIf"],[1,"form-group","mb-3"],["for","email"],[1,"col-12","p-0"],["type","email","formControlName","email","id","email","placeholder","Email",1,"form-control",3,"ngModelChange"],[4,"ngFor","ngForOf"],["for","password"],["type","password","formControlName","password","id","password","placeholder","Password",1,"form-control",3,"ngClass"],["class","invalid-feedback",4,"ngIf"],[1,"mt-3"],["type","submit",1,"btn","btn-primary","btn-block"],[1,"mt-4","text-center"],[1,"text-muted"],[1,"mdi","mdi-lock","mr-1"],["type","danger",3,"dismissible"],[1,"invalid-feedback"],[4,"ngIf"]],template:function(e,t){1&e&&(c.Pb(0,"div",0),c.Pb(1,"div",1),c.Pb(2,"div",2),c.Pb(3,"div",3),c.Pb(4,"div",4),c.Pb(5,"div",5),c.Pb(6,"div",6),c.Pb(7,"div",7),c.Pb(8,"div",8),c.Pb(9,"h5",9),c.Cc(10,"Welcome Back !"),c.Ob(),c.Pb(11,"p"),c.Cc(12,"Sign in to continue to your profile."),c.Ob(),c.Ob(),c.Ob(),c.Pb(13,"div",10),c.Lb(14,"img",11),c.Ob(),c.Ob(),c.Ob(),c.Pb(15,"div",12),c.Pb(16,"div"),c.Pb(17,"a",13),c.Pb(18,"div",14),c.Pb(19,"span",15),c.Lb(20,"img",16),c.Ob(),c.Ob(),c.Ob(),c.Ob(),c.Pb(21,"div",17),c.Pb(22,"form",18),c.ac("ngSubmit",(function(){return t.onSubmit()})),c.Ac(23,u,2,2,"ngb-alert",19),c.Pb(24,"div",20),c.Pb(25,"label",21),c.Cc(26,"Email"),c.Ob(),c.Pb(27,"div",22),c.Pb(28,"select",23),c.ac("ngModelChange",(function(e){return t.selectUser(e)})),c.Ac(29,b,2,1,"option",24),c.Ob(),c.Ob(),c.Ob(),c.Pb(30,"div",20),c.Pb(31,"label",25),c.Cc(32,"Password"),c.Ob(),c.Lb(33,"input",26),c.Ac(34,f,2,1,"div",27),c.Ob(),c.Pb(35,"div",28),c.Pb(36,"button",29),c.Cc(37,"Log In"),c.Ob(),c.Ob(),c.Pb(38,"div",30),c.Pb(39,"a",31),c.Lb(40,"i",32),c.Cc(41," Forgot your password?"),c.Ob(),c.Ob(),c.Ob(),c.Ob(),c.Ob(),c.Ob(),c.Ob(),c.Ob(),c.Ob(),c.Ob()),2&e&&(c.xb(22),c.hc("formGroup",t.loginForm),c.xb(1),c.hc("ngIf",t.error),c.xb(6),c.hc("ngForOf",t.users),c.xb(4),c.hc("ngClass",c.kc(5,g,t.submitted&&t.f.password.errors)),c.xb(1),c.hc("ngIf",t.submitted&&t.f.password.errors))},directives:[n.o,n.i,n.d,r.k,n.l,n.h,n.c,r.j,n.a,r.i,o.b,n.j,n.n],styles:[""]}),m)}],P=((h=function e(){_classCallCheck(this,e)}).\u0275mod=c.Ib({type:h}),h.\u0275inj=c.Hb({factory:function(e){return new(e||h)},imports:[[a.d.forChild(v)],a.d]}),h),y=((p=function e(){_classCallCheck(this,e)}).\u0275mod=c.Ib({type:p}),p.\u0275inj=c.Hb({factory:function(e){return new(e||p)},imports:[[r.b,n.k,o.c,s.a,P]]}),p)},jcJX:function(e,t,i){"use strict";i.r(t),i.d(t,"AccountModule",(function(){return b}));var r,n,o=i("ofXK"),s=i("tyNb"),a=i("fXoL"),c=[{path:"auth",loadChildren:function(){return Promise.resolve().then(i.bind(null,"cnSs")).then((function(e){return e.AuthModule}))}}],l=((r=function e(){_classCallCheck(this,e)}).\u0275mod=a.Ib({type:r}),r.\u0275inj=a.Hb({factory:function(e){return new(e||r)},imports:[[s.d.forChild(c)],s.d]}),r),u=i("cnSs"),b=((n=function e(){_classCallCheck(this,e)}).\u0275mod=a.Ib({type:n}),n.\u0275inj=a.Hb({factory:function(e){return new(e||n)},imports:[[o.b,l,u.AuthModule]]}),n)}}]);