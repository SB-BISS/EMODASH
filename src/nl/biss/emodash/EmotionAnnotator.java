package nl.biss.emodash;

import java.util.HashMap;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

/** 
 * 
 * The emotion annotator hides the complexity of 
 * dealing with Machine learning Web Services
 * 
 * Maybe we do not need this one as we can create a Python flask annotation service
 * 
 * @author Stefano
 *
 */
@RestController
public class EmotionAnnotator {
	
	
	
	
	
	@PostMapping("/annotate")
    public String annotate(@RequestParam("file") MultipartFile file) {
	
		
		// in here we need to call the model of EMODASH
		// possibly a flask webservice.
		// We expect to work in JSON
		// the MultipartFile should be the Wav of 3 or 4 secs.
		
		
		
		return null;
		
	}

	
	

}
