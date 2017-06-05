<?php
	function XSSdefenseForAttributeCase1($input){
		$escapeInput = "";
		if substr($input, "&quot;"){
			$input = str_replace("&quot;", "-", $input)
		}
		for($i=0; $i<strlen($input); $i++){
			switch($input[$i]){
				case '"':
					$escapeInput = $escapeInput . '-';
					break;
				default: 
					$escapeInput = $escapeInput . $input[$i];

		    }
        }

		$escapeInput = '"' . $escapeInput . '"';		

		return $escapeInput;
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
?>