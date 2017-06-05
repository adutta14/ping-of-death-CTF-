<?php
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
?>