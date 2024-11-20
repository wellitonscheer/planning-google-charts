set F := { 1,2,3,4,5}; # conjunto de indices das fabricas, em que a ultima corresponde ao centro de distribuicao
set P := {1,2,3,4,5};  # conjunto de indices dos produtos
set D := {0 .. 30};  # conjunto de indices dos dias
set K := {1 ..8};  # conjunto de indices dos veiculos

set Pi := {1,3,5};  # produtos primarios
set Pd := {2,4};  # produtos derivados;

set KP := K*P;

param FF[F*F] := <1,3> 1, <1,4> 1, <1,5> 1, <2,5> 1, <3,1> 1, <3,5> 1, <4,5> 1 default 0;
param TT[F*F] := <1,3> 1, <1,4> 2, <1,5> 2, <2,5> 2, <3,1> 1, <3,5> 2, <4,5> 1 default 0;
param CKP[KP] := <1,1> 21168, <2,1> 12960, <3,1> 21168, <4,1> 12096,  #capacidade do veiculo k para transportar o produto p 
                 <1,2> 22680, <2,2> 12960, <3,2> 22680, <4,2> 12960,
                 <5,5> 17192, 
                 <6,3> 28000, <7,3> 28000, <8,4> 150000 default 0; 
param FP[F*P] := <1,1> 1, <1,2> 1, <1,3> 1, <2,5> 1, <3,1> 1, <3,2> 1, <4,3> 1, <4,4> 1 default 0;

set FPD := { <f,p,d> in F*P*D with FP[f,p] == 1 or f == 5};
set FPiD := { <f,p,d> in F*Pi*D with FP[f,p] == 1 };
set FPDFK := { <f,p,d,fl,k> in F*P*D*F*K with f != fl and FF[f,fl] == 1 and CKP[k,p] > 0 and (FP[f,p] == 1 or f==5)};
set PP := { <p,pl> in P*P with p != pl};  
set PD := P*D;
set FPFK := { <f,p,fl,k> in F*P*F*K with f != fl and FF[f,fl] == 1 and CKP[k,p] > 0 and (FP[f,p] == 1 or f==5)};

param distancia[F*F] :=  <1,2> 57, <1,5> 441 default 99999; 
param co2[K] :=  <1> 0.5, <2> 0.4, <3> 0.66, <4> 1.1, <5> 1.43, <6> 1.8, <7> 0.8, <8> 0.9; 

param a[PP] := <1,2> 1, <3,4> 1 default 0;     # determina se o produto pl utiliza o produto p ceria prima
set FPiPdD := { <f,pi,pd,d> in F*Pi*Pd*D with  FP[f,pd] == 1  and a[pi,pd]==1 };om mat
param TQ[P] := <1> 20, <3> 3, <5> 5 default 0; # tempo de quarentena do produto
param Dem[P] := <1> 50000, <2> 50000, <3> 10000, <4> 50000, <5> 40000;
param CF[F*P] := <1,1> 37800, <1,2> 21420, <1,3> 50000, <2,5> 20000, <3,1> 18900, <3,2> 21420, 
                 <4,3> 50000, <4,4> 30000 default 0 ; 
param I0[F*P] := <1,2> 0 default 0;

var I[FPD] >=0;  # variavel do estoque do produto  p na fabrica f no dia d
var Q[<f,p,d> in FPD] >=0 <= if d <= TQ[p]+1 then 0 else Dem[p] end;  # variavel que determina a quantidade do produto p que eh liberada da quarentena no dia d na frab f
var yd[<f,pi,pd,d> in FPiPdD] >=0 <= CF[f,pd]; # var qtde produzida do produto p no dia d na frab f
var yi[<f,p,d> in FPiD] >=0 <= CF[f,p]; # var que determina a qtde produzida do produto p no dia d na frab f
var x[FPDFK] >=0; # variavel que determina a quantidade do produto p que sai da fab f e vai para a fab fl no no dia d 
var x2[<f,p,d,fl,k> in FPDFK] >=0 <= if d <= TT[f,fl] then 0 else Dem[p] end; # var que determina a qtde do produto p que chega na fab fl  vindo da fab f no no dia d 
var Tmax >=0 ; #<= valorDoUB;
var w[PD] binary;
var z[FPDFK] binary;

minimize fo : Tmax + 
              #sum <f,p,d,fl,k> in FPDFK : distancia[f,fl] * co2[k] * x[f,p,d,fl,k] +
              0.0001 * sum <f,p,d> in FPiD : yi[f,p,d];

subto c1a: forall <f,p,d> in FPD with d > 0 and f < 5 do
             I[f,p,d] == I[f,p,d-1] + Q[f,p,d] + sum<fl,p,d,f,k> in FPDFK : x2[fl,p,d,f,k] 
                        - sum <f,p,d,fl,k> in FPDFK : x[f,p,d,fl,k] 
                        - sum <f,p,pd,d> in FPiPdD :  yd[f,p,pd,d]; 

subto c1b: forall <f,p,d> in FPD with d > 0 do # tem q enviar em ate 7 dias devido a ser perecivel 
              Q[f,p,d] <= sum <f,p,dl,fl,k> in FPDFK with dl >= d and dl <= d+6: x[f,p,d,fl,k] 
                        + sum <f,p,pd,dl> in FPiPdD with dl >= d and dl <= d+6:  yd[f,p,pd,dl]; 
 
subto c2a: forall <f,pi,pd,d> in FPiPdD with d + TQ[pd]+1 <= card(D)-1 do
             yd[f,pi,pd,d] == Q[f,pd,d+TQ[pd]+1];

subto c2b: forall <f,p,d> in FPiD with d + TQ[p]+1   <= card(D)-1 do
             yi[f,p,d] == Q[f,p,d+TQ[p]+1];

subto c2c: forall <f,p,d,fl,k> in FPDFK with d + TT[f,fl]  <= card(D)-1 do
              x[f,p,d,fl,k] == x2[f,p,d+TT[f,fl],fl,k];

subto c3: forall <f,p,d,fl,k> in FPDFK do
             x[f,p,d,fl,k] <= CKP[k,p];  # necessario considerar o tempo de transporte 

subto c4: forall <5,p,d> in FPD with d > 0 do  # restricao referente ao estoque no CD
             I[5,p,d] == I[5,p,d-1] +  sum <f,p,d,5,k> in FPDFK : x2[f,p,d,5,k]; 
                        
subto c5: forall <p> in P do 
           sum <p,d> in PD : w[p,d] == 1; 

subto c6: forall <5,p,d> in FPD do 
             I[5,p,d] >=  Dem[p] * w[p,d]; 

subto c7: forall <p,d> in PD do
             d*w[p,d] <= Tmax;

subto c8: forall <f> in F with f < 5 do  # estoque inicial
             forall <p> in P with FP[f,p] == 1 do
                I[f,p,0] == I0[f,p];

subto c9: forall <p> in P do  # estoque inicial no CD
                I[5,p,0] == I0[5,p];

subto c10: forall <f,p,d,fl,k> in FPDFK do 
              x[f,p,d,fl,k] <= CKP[k,p] * z[f,p,d,fl,k];

subto c11: forall <f,p,fl,k> in  FPFK with TT[f,fl] > 1 do
              forall <d> in D with d > 0 do
                 sum<f,p,dl,fl,k> in FPDFK with dl >= d and dl <=d+TT[f,fl]-1 : z[f,p,dl,fl,k] <= 1; 

