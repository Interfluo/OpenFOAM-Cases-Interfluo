clc; close all; clear all;
%INPUT VALUES
p_1 = xlsread('PARAMS.xlsx','PARAMETERS','B2');     %CHAMBER PRESSURE
T_1 = xlsread('PARAMS.xlsx','PARAMETERS','B3');     %CHAMBER TEMP
FT = xlsread('PARAMS.xlsx','PARAMETERS','B4');      %DESIRED THRUST OR....
m_dot = xlsread('PARAMS.xlsx','PARAMETERS','B5');   %DESIRED MASS FLOW RATE....
ALT = xlsread('PARAMS.xlsx','PARAMETERS','B6');     %ALTITUDE
g = xlsread('PARAMS.xlsx','PARAMETERS','B7');       %GAMMA
R = xlsread('PARAMS.xlsx','PARAMETERS','B8');       %GAS CONSTANT    
TR = xlsread('PARAMS.xlsx','PARAMETERS','B9'); %throat radius (cm)

%% exit pressure
if (11000>ALT) && (ALT<25000)
    T = -56.46; %C
    p_o = 1000*(22.65*exp(1.73-0.000157*ALT));
elseif ALT>=25000
    T = -131.21 + 0.00299*ALT ;
    p_o = 1000*(2.488*((T+273.1)/216.6)^-11.388);
else 
    T = 15.04 - 0.00649*ALT;
    p_o = 1000*(101.29*((T+273.1)/288.08)^5.256);
end

%%  begin calculation
PR = p_o/p_1;
PR2 = (p_o/p_1)^((g-1)/g);
TT = (2*g*R*T_1)/(g-1);
p_t = ((2/(g+1))^(g/(g-1)))*2.068;
v_t = sqrt((2*g*R*T_1)/(g+1));
v_e = sqrt(TT*(1-PR2));

if m_dot==0
    m_dot=FT/v_e;
elseif FT==0
    FT = m_dot/v_e;
else
    fprintf('You can either set desired thrust OR mass flow rate')
end

T_e = T_1*(p_o/p_1)^((g-1)/g);
a_e = sqrt(g*R*T_e);

Me = v_e/a_e;
    
% MOC
RTOD = 180/pi;
DTOR = pi/180;
P = []; %x axis points
%% PM FUNCTION
A = sqrt((g+1)/(g-1));
B = (g-1)/(g+1);
v_PM = @(x) A*atan(sqrt(B*(x^2-1))) - atan(sqrt(x^2-1));


%% CALCULATE T_MAX, BREAK UP INTO DIVISIONS
T_max = 0.5*v_PM(Me)*RTOD;
DT = (90-T_max) - fix(90-T_max);
T(1) = DT*DTOR;
n = T_max*2;

for m = 2:n+1
    T(m) = (DT + (m-1))*DTOR;
    %Mach from T(i) using T(i) = v_PM (FALSE POSITION)
    x_int = [1 1.01*Me];
    func = @(x) T(m) - v_PM(x);
    M(m) = fzero(func,x_int);
    P(m) = 0 + TR*tan(T(m)); %X-AXIS POINTS
    %RRSLOPES
    RR(m) = -TR/P(m);
    %LR slopes
    LR(m) = tan(T(m)+asin(1/M(m)));
    SL(m) = -RR(m);
end
%% PLOTTING
P(1) = [];
l = length(P);

for j = 1:l
    P1 = [0 TR];
    P2 = [P(j) 0];
    plot(P2,P1,'k')
    hold on
    xlabel('CENTERLINE')
    ylabel('RADIUS')
end
hold on;
LR(1) = []; RR(1) = [];
SL(1) = [];
F = RR(m-1);

for c = 1:length(P)-1
    x(c) = (TR+SL(c)*P(c))/(SL(c)-F);
    y(c) = F*x(c)+TR;
    X_P = [P(c) x(c)];
    Y_P = [0 y(c)];
    plot(X_P,Y_P,'b');
end
hold on

%% FIRST WALL SECTION
TM = T_max*DTOR;
xw(1) = (TR+SL(1)*P(1))/(SL(1)-tan(TM));
yw(1) = tan(TM)*xw(1)+TR;
X_P2 = [P(1) xw];
Y_P2 = [P(2) yw];
plot(X_P2,Y_P2,'g');
%DIVIDE (delta slopes)
DTW = tan(TM)/(length(P)-1);
s(1) = tan(TM);
b(1) = TR;

for k = 2:length(P)-1
  s(k) = tan(TM)-(k-1)*DTW; %slope
  b(k) = yw(k-1)-s(k)*xw(k-1); %y-int
  xw(k) = (b(k)+SL(k)*P(k))/(SL(k)-s(k));
  yw(k) = s(k)*xw(k)+b(k);
  X_P3 = [x(k) xw(k)];
  Y_P3 = [y(k) yw(k)];
  plot(X_P3,Y_P3,'r');
end
hold on
xf = (b(length(b))+SL(length(SL))*P(length(P)))/SL(length(SL));
yf = b(length(b));
X_F = [P(length(P)) xf];
Y_F = [0 yf];
plot(X_F,Y_F,'r');
xw = [0 xw];
yw = [TR yw];

%% Write the results to file
xlswrite('PARAMS.xlsx',transpose(xw),'PTS','A1:A62');
xlswrite('PARAMS.xlsx',transpose(yw),'PTS','B1:B62');
    
