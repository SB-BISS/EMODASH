package nl.biss.emodash;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurerAdapter;

@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
    
    @Bean
    public WebMvcConfigurer corsConfigurer() {
        return new WebMvcConfigurerAdapter() {
        	@Override
            public void addCorsMappings(CorsRegistry registry) {
                registry.addMapping("/get_anagraphic_data").allowedOrigins("*");
                registry.addMapping("/get_customer_ids").allowedOrigins("*");
                registry.addMapping("/customer_lastcall").allowedOrigins("*");
                registry.addMapping("/agent_lastcall").allowedOrigins("*");
                registry.addMapping("/get_call_id_with_customer").allowedOrigins("*");
                registry.addMapping("/customer_emotions_live").allowedOrigins("*");
                
            }
        };
    }
    
    
}
