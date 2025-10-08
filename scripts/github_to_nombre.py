# Mapeo de usuario GitHub a nombre completo
# Formato: "usuario_github": "NOMBRE COMPLETO"
def c_nombre(nombre):
    return ' '.join([p.capitalize() for p in nombre.split()])

github_to_nombre = {
    "thaineaas": c_nombre("ALARCON SEGOVIA THAINE ALEXANDER"),
    "andNiAl": c_nombre("ALVA CHAVEZ ANDREA NIKOLE"),
    "Julio3008": c_nombre("ANTAURCO MUNDO JULIO ALEXANDER"),
    "leonardoPBF": c_nombre("BUITRON FARFAN LEONARDO PAUL"),
    "Adriancas28": c_nombre("CASTRO ORTIZ ELMER ADRIAN"),
    "DiegoCervantes1303": c_nombre("CERVANTES CASTILLON DIEGO FRANCISCO"),
    "carlofav12": c_nombre("CHAVARRIA ROJAS CARLO FABRIZIO"),
    "melivezla": c_nombre("CHAVEZ LAIME MELISSA ROCIO"),
    "CorillaFrank": c_nombre("CORILLA YANGALI FRANK LUIS"),
    "PachamancaUwu": c_nombre("CUETO ESCOBAR MATHIAS MARCELO"),
    "PieroDev23": c_nombre("DAVILA AGUIRRE PIERO ALONSO FRANCESCO"),
    "Ghostcito": c_nombre("GUTIERREZ CASANI JUAN MATIAS"),
    "ediso9": c_nombre("GUTIERREZ CORDOVA EDISON ARTURO"),
    "RobinsonHL18": c_nombre("HERRERA LOPEZ JAVIER ROBINSON"),
    "eduardo0804": c_nombre("LAZARO BRAVO JESUS EDUARDO"),
    "JeanClix": c_nombre("LOBATON OCHOA JEAN PIERRE ANTHONY"),
    "luismll111": c_nombre("MAMANI LLANLLAYA LUIS MIGUEL"),
    "JoshMartinezB99": c_nombre("MARTINEZ BLANCO JOSHUA FABIANNI"),
    "MarkoSebass": c_nombre("ORIHUELA CARRASCO MARKO SEBASTIAN"),
    "MichaelG003": c_nombre("ORIHUELA TOMATEO MICHAEL GUSTAVO MILNER"),
    "JhowillSC": c_nombre("ORO ANTICONA JHONATAN GERARD"),
    "Andramir99": c_nombre("PANDURO ALVAREZ MARCELO ANDRE"),
    "OscarPineda1": c_nombre("PINEDA FLORES OSCAR RENE"),
    "RoNaLd82QS": c_nombre("QUISPE OSCCO RONALD ANTHONY"),
    "Mary123987": c_nombre("ROJAS CORDOVA MARY ELIANE"),
    "tatiana17899": c_nombre("SUAREZ ROSAS TATIANA MERCEDES"),
    "ticopera207": c_nombre("TICONA PERALTA LUIS RAUL"),
    "Cetok": c_nombre("TORVISCO RIOS JUAN MARCIAL"),
    "juancavite97": c_nombre("VITE AGURTO JUAN CARLOS"),
    "GeraYF": c_nombre("YANQUE FLORES GERALDINE LOANA"),
    "Leonardo-YC": c_nombre("YUPAN CRUZ JOSE LEONARDO")
}
