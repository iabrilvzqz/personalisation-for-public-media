(window.webpackJsonp=window.webpackJsonp||[]).push([[6],{cnSs:function(t,e,r){"use strict";r.r(e),r.d(e,"AuthModule",(function(){return h}));var i=r("ofXK"),n=r("3Pt+"),o=r("1kSV"),s=r("4zvT"),a=r("tyNb"),b=r("fXoL"),c=r("7dP1");function l(t,e){if(1&t&&(b.Pb(0,"ngb-alert",33),b.Cc(1),b.Ob()),2&t){const t=b.cc();b.hc("dismissible",!1),b.xb(1),b.Dc(t.error)}}function d(t,e){if(1&t&&(b.Pb(0,"option"),b.Cc(1),b.Ob()),2&t){const t=e.$implicit;b.xb(1),b.Dc(t.email)}}function u(t,e){1&t&&(b.Pb(0,"div"),b.Cc(1,"Password is required"),b.Ob())}function m(t,e){if(1&t&&(b.Pb(0,"div",34),b.Ac(1,u,2,0,"div",35),b.Ob()),2&t){const t=b.cc();b.xb(1),b.hc("ngIf",t.f.password.errors.required)}}const f=function(t){return{"is-invalid":t}},p=[{path:"login",component:(()=>{class t{constructor(t,e,r,i){this.formBuilder=t,this.route=e,this.router=r,this.authenticationService=i,this.submitted=!1,this.error="",this.year=(new Date).getFullYear(),this.users=[{id:2,email:"albert@students.uu.nl",picture:"avatar-1.jpg",type:"Content Devourer"},{id:3,email:"ilse@students.uu.nl",picture:"avatar-2.jpg",type:"Series Streamer"},{id:4,email:"kevine@students.uu.nl",picture:"avatar-3.jpg",type:"Movie Buff"},{id:7,email:"enrique@students.uu.nl",picture:"avatar-4.jpg",type:"Documentary Lover"}]}ngOnInit(){this.loginForm=this.formBuilder.group({email:["albert@students.uu.nl",[n.m.required,n.m.email]],password:["123456",[n.m.required]]}),this.selectUser(this.users[0].email),this.returnUrl=this.route.snapshot.queryParams.returnUrl||"/"}ngAfterViewInit(){}get f(){return this.loginForm.controls}onSubmit(){this.submitted=!0,this.loginForm.invalid||(this.authenticationService.login(this.selectedUser),this.router.navigate(["/dashboard"]))}getUserInformation(t){return this.users.filter(e=>e.email===t)[0]}selectUser(t){this.selectedUser=this.getUserInformation(t)}}return t.\u0275fac=function(e){return new(e||t)(b.Kb(n.b),b.Kb(a.a),b.Kb(a.c),b.Kb(c.a))},t.\u0275cmp=b.Eb({type:t,selectors:[["app-login"]],decls:42,vars:7,consts:[[1,"account-pages","mt-5","mb-5"],[1,"container"],[1,"row","justify-content-center"],[1,"col-md-8","col-lg-6","col-xl-5"],[1,"card","overflow-hidden"],[1,"bg-soft-primary"],[1,"row"],[1,"col-7"],[1,"text-primary","p-4"],[1,"text-primary"],[1,"col-5","align-self-end"],["src","assets/images/profile-img.png","alt","",1,"img-fluid"],[1,"card-body","pt-0"],["href","/"],[1,"avatar-md","profile-user-wid","mb-4"],[1,"avatar-title","rounded-circle","bg-dark"],["src","assets/images/logo-light-sm.svg","alt","","height","34",1,"rounded-circle"],[1,"p-2"],[1,"form-horizontal",3,"formGroup","ngSubmit"],["type","danger",3,"dismissible",4,"ngIf"],[1,"form-group","mb-3"],["for","email"],[1,"col-12","p-0"],["type","email","formControlName","email","id","email","placeholder","Email",1,"form-control",3,"ngModelChange"],[4,"ngFor","ngForOf"],["for","password"],["type","password","formControlName","password","id","password","placeholder","Password",1,"form-control",3,"ngClass"],["class","invalid-feedback",4,"ngIf"],[1,"mt-3"],["type","submit",1,"btn","btn-primary","btn-block"],[1,"mt-4","text-center"],[1,"text-muted"],[1,"mdi","mdi-lock","mr-1"],["type","danger",3,"dismissible"],[1,"invalid-feedback"],[4,"ngIf"]],template:function(t,e){1&t&&(b.Pb(0,"div",0),b.Pb(1,"div",1),b.Pb(2,"div",2),b.Pb(3,"div",3),b.Pb(4,"div",4),b.Pb(5,"div",5),b.Pb(6,"div",6),b.Pb(7,"div",7),b.Pb(8,"div",8),b.Pb(9,"h5",9),b.Cc(10,"Welcome Back !"),b.Ob(),b.Pb(11,"p"),b.Cc(12,"Sign in to continue to your profile."),b.Ob(),b.Ob(),b.Ob(),b.Pb(13,"div",10),b.Lb(14,"img",11),b.Ob(),b.Ob(),b.Ob(),b.Pb(15,"div",12),b.Pb(16,"div"),b.Pb(17,"a",13),b.Pb(18,"div",14),b.Pb(19,"span",15),b.Lb(20,"img",16),b.Ob(),b.Ob(),b.Ob(),b.Ob(),b.Pb(21,"div",17),b.Pb(22,"form",18),b.ac("ngSubmit",(function(){return e.onSubmit()})),b.Ac(23,l,2,2,"ngb-alert",19),b.Pb(24,"div",20),b.Pb(25,"label",21),b.Cc(26,"Email"),b.Ob(),b.Pb(27,"div",22),b.Pb(28,"select",23),b.ac("ngModelChange",(function(t){return e.selectUser(t)})),b.Ac(29,d,2,1,"option",24),b.Ob(),b.Ob(),b.Ob(),b.Pb(30,"div",20),b.Pb(31,"label",25),b.Cc(32,"Password"),b.Ob(),b.Lb(33,"input",26),b.Ac(34,m,2,1,"div",27),b.Ob(),b.Pb(35,"div",28),b.Pb(36,"button",29),b.Cc(37,"Log In"),b.Ob(),b.Ob(),b.Pb(38,"div",30),b.Pb(39,"a",31),b.Lb(40,"i",32),b.Cc(41," Forgot your password?"),b.Ob(),b.Ob(),b.Ob(),b.Ob(),b.Ob(),b.Ob(),b.Ob(),b.Ob(),b.Ob(),b.Ob()),2&t&&(b.xb(22),b.hc("formGroup",e.loginForm),b.xb(1),b.hc("ngIf",e.error),b.xb(6),b.hc("ngForOf",e.users),b.xb(4),b.hc("ngClass",b.kc(5,f,e.submitted&&e.f.password.errors)),b.xb(1),b.hc("ngIf",e.submitted&&e.f.password.errors))},directives:[n.o,n.i,n.d,i.k,n.l,n.h,n.c,i.j,n.a,i.i,o.b,n.j,n.n],styles:[""]}),t})()}];let g=(()=>{class t{}return t.\u0275mod=b.Ib({type:t}),t.\u0275inj=b.Hb({factory:function(e){return new(e||t)},imports:[[a.d.forChild(p)],a.d]}),t})(),h=(()=>{class t{}return t.\u0275mod=b.Ib({type:t}),t.\u0275inj=b.Hb({factory:function(e){return new(e||t)},imports:[[i.b,n.k,o.c,s.a,g]]}),t})()},jcJX:function(t,e,r){"use strict";r.r(e),r.d(e,"AccountModule",(function(){return c}));var i=r("ofXK"),n=r("tyNb"),o=r("fXoL");const s=[{path:"auth",loadChildren:()=>Promise.resolve().then(r.bind(null,"cnSs")).then(t=>t.AuthModule)}];let a=(()=>{class t{}return t.\u0275mod=o.Ib({type:t}),t.\u0275inj=o.Hb({factory:function(e){return new(e||t)},imports:[[n.d.forChild(s)],n.d]}),t})();var b=r("cnSs");let c=(()=>{class t{}return t.\u0275mod=o.Ib({type:t}),t.\u0275inj=o.Hb({factory:function(e){return new(e||t)},imports:[[i.b,a,b.AuthModule]]}),t})()}}]);