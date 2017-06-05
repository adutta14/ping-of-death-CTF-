<?php 
	
	//To handle case for attribute=<malicious code> code 
	function XSSdefenseForAttributeCase1($input){
		$escapeInput = "";
		for($i=0; $i<strlen($input); $i++){
			switch($input[$i]){
				case '"':
                case '&quot;':
					$escapeInput = $escapeInput . '-';
					break;
				default: 
					$escapeInput = $escapeInput . $input[$i];

		    }
        }

		$escapeInput = '"' . $escapeInput . '"';		

		return $escapeInput;
	}
            
	//echo XSSdefenseForAttributeCase1('abcde&quot;');



	function sqlSpecialChars($input){
		for($i=0; $i<strlen($input); $i++){
			switch($input[$i]){
				case ';':
				case "'":
				case '"':
				case '=':
					$input = substr($input, 0, $i) . '\\' . substr($input, $i);
					$i = $i+1;
				break;

				case '-':
					if($input[$i+1] == '-'){
						$input[$i] = '0';
						$input[$i+1] = '0';
					}
				break;
			}
		}
		return $input;
	}


	function sqlSpecialKeyWords($input){
		$splitedInput = explode(' ', $input);
		for($i=0; $i<count($splitedInput); $i++){
			$string = $splitedInput[$i];
			$string = strtolower($string);
			switch($string){
				case 'select':
				case 'insert':
				case 'update':
				case 'delete':
				case 'union':
					$splitedInput[$i] = '\\' + $splitedInput[$i];
			}
		}

		return implode(" ", $splitedInput); 
	}

	function htmlSpecialCharacters($input){
		$string = htmlspecialchars($input);
		return $string;
	}

	// I kept this function independent of htmlspecialchars intentionally for other usages.
	function htmlRemoveSpecialCharacters($input){
		for($i=0; $i<strlen($input); $i++){

			$value = ord($input[$i]);
			if($value >= 48 && $value <= 57);
			elseif ($value >= 65 && $value <= 90) ;
			elseif ($value >= 97 && $value <= 122) ;
			elseif ($value == 32) ;
			else{
				$input = substr($input, 0, $i) . '\\' . substr($input, $i);
			}
		}
		echo $input;
		return $input;
	}

	function osCommandOverride($input){
		$input = escapeshellarg($input);
		return $input;
	}



?>