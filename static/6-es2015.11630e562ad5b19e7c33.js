(window.webpackJsonp=window.webpackJsonp||[]).push([[6],{cnSs:function(e,t,r){"use strict";r.r(t),r.d(t,"AuthModule",(function(){return h}));var i=r("ofXK"),o=r("3Pt+"),n=r("1kSV"),s=r("4zvT"),a=r("tyNb"),c=r("fXoL"),b=r("7dP1");function l(e,t){if(1&e&&(c.Pb(0,"ngb-alert",33),c.Ac(1),c.Ob()),2&e){const e=c.cc();c.fc("dismissible",!1),c.xb(1),c.Bc(e.error)}}function d(e,t){if(1&e&&(c.Pb(0,"option"),c.Ac(1),c.Ob()),2&e){const e=t.$implicit;c.xb(1),c.Bc(e.email)}}function u(e,t){1&e&&(c.Pb(0,"div"),c.Ac(1,"Password is required"),c.Ob())}function m(e,t){if(1&e&&(c.Pb(0,"div",34),c.yc(1,u,2,0,"div",35),c.Ob()),2&e){const e=c.cc();c.xb(1),c.fc("ngIf",e.f.password.errors.required)}}const f=function(e){return{"is-invalid":e}},p=[{path:"login",component:(()=>{class e{constructor(e,t,r,i){this.formBuilder=e,this.route=t,this.router=r,this.authenticationService=i,this.submitted=!1,this.error="",this.year=(new Date).getFullYear(),this.users=[{id:0,email:"nelson@email.com",picture:"avatar-1.jpg",type:"Content Devourer"},{id:1,email:"yara@email.com",picture:"avatar-2.jpg",type:"Series Streamer"},{id:4,email:"zeynep@email.com",picture:"avatar-3.jpg",type:"Movie Buff"},{id:7,email:"ojvind@email.com",picture:"avatar-4.jpg",type:"Documentary Lover"}]}ngOnInit(){this.loginForm=this.formBuilder.group({email:["nelson@email.com",[o.m.required,o.m.email]],password:["123456",[o.m.required]]}),this.selectUser(this.users[0].email),this.returnUrl=this.route.snapshot.queryParams.returnUrl||"/"}ngAfterViewInit(){}get f(){return this.loginForm.controls}onSubmit(){this.submitted=!0,this.loginForm.invalid||(this.authenticationService.login(this.selectedUser),this.router.navigate(["/dashboard"]))}getUserInformation(e){return this.users.filter(t=>t.email===e)[0]}selectUser(e){this.selectedUser=this.getUserInformation(e)}}return e.\u0275fac=function(t){return new(t||e)(c.Kb(o.b),c.Kb(a.a),c.Kb(a.c),c.Kb(b.a))},e.\u0275cmp=c.Eb({type:e,selectors:[["app-login"]],decls:42,vars:7,consts:[[1,"account-pages","mt-5","mb-5"],[1,"container"],[1,"row","justify-content-center"],[1,"col-md-8","col-lg-6","col-xl-5"],[1,"card","overflow-hidden"],[1,"bg-soft-primary"],[1,"row"],[1,"col-7"],[1,"text-primary","p-4"],[1,"text-primary"],[1,"col-5","align-self-end"],["src","assets/images/profile-img.png","alt","",1,"img-fluid"],[1,"card-body","pt-0"],["href","/"],[1,"avatar-md","profile-user-wid","mb-4"],[1,"avatar-title","rounded-circle","bg-dark"],["src","assets/images/logo-light-sm.svg","alt","","height","34",1,"rounded-circle"],[1,"p-2"],[1,"form-horizontal",3,"formGroup","ngSubmit"],["type","danger",3,"dismissible",4,"ngIf"],[1,"form-group","mb-3"],["for","email"],[1,"col-12","p-0"],["type","email","formControlName","email","id","email","placeholder","Email",1,"form-control",3,"ngModelChange"],[4,"ngFor","ngForOf"],["for","password"],["type","password","formControlName","password","id","password","placeholder","Password",1,"form-control",3,"ngClass"],["class","invalid-feedback",4,"ngIf"],[1,"mt-3"],["type","submit",1,"btn","btn-primary","btn-block"],[1,"mt-4","text-center"],[1,"text-muted"],[1,"mdi","mdi-lock","mr-1"],["type","danger",3,"dismissible"],[1,"invalid-feedback"],[4,"ngIf"]],template:function(e,t){1&e&&(c.Pb(0,"div",0),c.Pb(1,"div",1),c.Pb(2,"div",2),c.Pb(3,"div",3),c.Pb(4,"div",4),c.Pb(5,"div",5),c.Pb(6,"div",6),c.Pb(7,"div",7),c.Pb(8,"div",8),c.Pb(9,"h5",9),c.Ac(10,"Welcome Back !"),c.Ob(),c.Pb(11,"p"),c.Ac(12,"Sign in to continue to your profile."),c.Ob(),c.Ob(),c.Ob(),c.Pb(13,"div",10),c.Lb(14,"img",11),c.Ob(),c.Ob(),c.Ob(),c.Pb(15,"div",12),c.Pb(16,"div"),c.Pb(17,"a",13),c.Pb(18,"div",14),c.Pb(19,"span",15),c.Lb(20,"img",16),c.Ob(),c.Ob(),c.Ob(),c.Ob(),c.Pb(21,"div",17),c.Pb(22,"form",18),c.ac("ngSubmit",(function(){return t.onSubmit()})),c.yc(23,l,2,2,"ngb-alert",19),c.Pb(24,"div",20),c.Pb(25,"label",21),c.Ac(26,"Email"),c.Ob(),c.Pb(27,"div",22),c.Pb(28,"select",23),c.ac("ngModelChange",(function(e){return t.selectUser(e)})),c.yc(29,d,2,1,"option",24),c.Ob(),c.Ob(),c.Ob(),c.Pb(30,"div",20),c.Pb(31,"label",25),c.Ac(32,"Password"),c.Ob(),c.Lb(33,"input",26),c.yc(34,m,2,1,"div",27),c.Ob(),c.Pb(35,"div",28),c.Pb(36,"button",29),c.Ac(37,"Log In"),c.Ob(),c.Ob(),c.Pb(38,"div",30),c.Pb(39,"a",31),c.Lb(40,"i",32),c.Ac(41," Forgot your password?"),c.Ob(),c.Ob(),c.Ob(),c.Ob(),c.Ob(),c.Ob(),c.Ob(),c.Ob(),c.Ob(),c.Ob()),2&e&&(c.xb(22),c.fc("formGroup",t.loginForm),c.xb(1),c.fc("ngIf",t.error),c.xb(6),c.fc("ngForOf",t.users),c.xb(4),c.fc("ngClass",c.ic(5,f,t.submitted&&t.f.password.errors)),c.xb(1),c.fc("ngIf",t.submitted&&t.f.password.errors))},directives:[o.o,o.i,o.d,i.k,o.l,o.h,o.c,i.j,o.a,i.i,n.b,o.j,o.n],styles:[""]}),e})()}];let g=(()=>{class e{}return e.\u0275mod=c.Ib({type:e}),e.\u0275inj=c.Hb({factory:function(t){return new(t||e)},imports:[[a.d.forChild(p)],a.d]}),e})(),h=(()=>{class e{}return e.\u0275mod=c.Ib({type:e}),e.\u0275inj=c.Hb({factory:function(t){return new(t||e)},imports:[[i.b,o.k,n.c,s.a,g]]}),e})()},jcJX:function(e,t,r){"use strict";r.r(t),r.d(t,"AccountModule",(function(){return b}));var i=r("ofXK"),o=r("tyNb"),n=r("fXoL");const s=[{path:"auth",loadChildren:()=>Promise.resolve().then(r.bind(null,"cnSs")).then(e=>e.AuthModule)}];let a=(()=>{class e{}return e.\u0275mod=n.Ib({type:e}),e.\u0275inj=n.Hb({factory:function(t){return new(t||e)},imports:[[o.d.forChild(s)],o.d]}),e})();var c=r("cnSs");let b=(()=>{class e{}return e.\u0275mod=n.Ib({type:e}),e.\u0275inj=n.Hb({factory:function(t){return new(t||e)},imports:[[i.b,a,c.AuthModule]]}),e})()}}]);