<html>
<head>
<style>
textarea{
	width:70%;
	height:40%;
}
</style>
</head>
<body>
<center>
rules:<br>
<textarea id="rules">
AFG_Afghanistan
ALB_Albania
ALG_Algeria
ARG_Argentina
ARM_Armenia
AUS_Australia
AUT_Austria
AZE_Azerbaijan
BAH_Bahrain
BGD_Bangladesh
BLR_Belarus
BEL_Belgium
BEN_Benin
BOL_Bolivia
BIH_Bosnia and Herzegovina
BWA_Botswana
BRA_Brazil
BRU_Brunei
BGR_Bulgaria
BFA_Burkina Faso
KHM_Cambodia
CAN_Canada
CHI_Chile
CHN_Republic of China \(Taiwan\)
CHN_People's Republic of China
CHN_China
COL_Colombia
CIS_Commonwealth of Independent States
CRI_Costa Rica
HRV_Croatia
CUB_Cuba
CYP_Cyprus
CZE_Czech Republic
CZS_Czechoslovakia
DEN_Denmark
ECU_Ecuador
EGY_Egypt
EST_Estonia
FIN_Finland
FRA_France
GMB_Gambia
GEO_Georgia
GDR_German Democratic Republic
GER_Germany
GHA_Ghana
HEL_Greece
GTM_Guatemala
HND_Honduras
HKG_Hong Kong
HUN_Hungary
ISL_Iceland
IND_India
IDN_Indonesia
IRQ_Iraq
IRN_Islamic Republic of Iran
IRN_Iran
IRL_Ireland
ISR_Israel
ITA_Italy
CIV_Ivory Coast
JPN_Japan
KAZ_Kazakhstan
KAZ_Kazakhstan
KEN_Kenya
PRK_Democratic People's Republic of Korea
KOR_Republic of Korea
KSV_Kosovo
KWT_Kuwait
KGZ_Kyrgyzstan
LVA_Latvia
LIE_Liechtenstein
LTU_Lithuania
LUX_Luxembourg
MAC_Macao-China
MAC_Macau
MAC_Macao
MKD_The former Yugoslav Republic of Macedonia
MKD_Macedonia
MDG_Madagascar
MAS_Malaysia
MRT_Mauritania
MEX_Mexico
MDA_Moldova
MNG_Mongolia
MNE_Montenegro
MAR_Morocco
MOZ_Mozambique
MMR_Myanmar
NLD_Netherlands
NZL_New Zealand
NPL_Nepal
NIC_Nicaragua
NGA_Nigeria
NOR_Norway
PAK_Pakistan
PAN_Panama
PAR_Paraguay
PER_Peru
PHI_Philippines
POL_Poland
POR_Portugal
PRI_Puerto Rico
ROU_Romania
RUS_Russian Federation
RUS_Russia
SLV_El Salvador
SAU_Saudi Arabia
SEN_Senegal
SRB_Serbia
SCG_Serbia and Montenegro
SGP_Singapore
SVK_Slovakia
SVN_Slovenia
SAF_South Africa
ESP_Spain
LKA_Sri Lanka
SWE_Sweden
SUI_Switzerland
SUR_Suriname
SYR_Syria
TWN_Taiwan
TWN_Chinese Taipei
TJK_Tajikistan
TZA_Tanzania
THA_Thailand
TTO_Trinidad and Tobago
TUN_Tunisia
TUR_Turkey
NCY_Turkish Republic of Northern Cyprus
TKM_Turkmenistan
UGA_Uganda
UKR_Ukraine
UAE_United Arab Emirates
UNK_United Kingdom
USA_United States of America
USA_United States
URY_Uruguay
USS_Union of Soviet Socialist Republics
USS_Soviet Union
UZB_Uzbekistan
VEN_Venezuela
VNM_Vietnam
VNM_Viet Nam
YUG_Yugoslavia
ZWE_Zimbabwe
_Republic of </textarea><br>
<input type="submit" value="run" onclick="run()"><br>
<textarea id="text"></textarea>
<br>
<input type="submit" onclick="namecodefix()" value="fix name-code">
</center>
<script>
run=function(){
	foo=rules.value.split("\n");
	for(var i=0;i<foo.length;i++){
		text.value=text.value.replace(new RegExp(foo[i].split("_")[1], 'g'), foo[i].split("_")[0]);
	}
}
namecodefix=function(){
	var kekolar = JSON.parse(text.value);
	for(var i=0;i<kekolar.length;i++){
		var foo = kekolar[i].code.split(" ");
		if(foo.length>1) {
			for(var j=0;j<foo.length-1;j++){
				kekolar[i].name+=" "+foo[j];
			}
			kekolar[i].code = foo[foo.length-1];
		}
	}
	text.value=JSON.stringify(kekolar);
	text.value=text.value.replace(/\}\,\{/g,"},\n{");
}
</script>
</body>
</html>